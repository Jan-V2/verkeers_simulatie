using System;
using System.IO;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Net.WebSockets;
using System.Threading;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;

namespace Controller
{
    class Program
    {
        private const string serverAdress = "ws://127.0.0.1:6969";
        static async Task Main(string[] args)
        {
            do
            {
                using (var socket = new ClientWebSocket())
                    try
                    {
                        await socket.ConnectAsync(new Uri(serverAdress), CancellationToken.None);
                        Console.WriteLine("connected");
                        //await Send(socket, "data");
                        await Receive(socket);
                        

                    }
                    catch (Exception ex)
                    {
                        Console.WriteLine($"ERROR - {ex.Message}");
                        Thread.Sleep(1000);

                    }
            } while (true);
        }

        static async Task Send(ClientWebSocket socket, string data) =>
            await socket.SendAsync(Encoding.UTF8.GetBytes(data), WebSocketMessageType.Text, true, CancellationToken.None);

        static async Task Receive(ClientWebSocket socket)
        {
            var buffer = new ArraySegment<byte>(new byte[2048]);
            do
            {
                WebSocketReceiveResult result;
                using (var ms = new MemoryStream())
                {
                    do
                    {
                        result = await socket.ReceiveAsync(buffer, CancellationToken.None);
                        ms.Write(buffer.Array, buffer.Offset, result.Count);
                    } while (!result.EndOfMessage);

                    if (result.MessageType == WebSocketMessageType.Close)
                        break;

                    ms.Seek(0, SeekOrigin.Begin);
                    using (var reader = new StreamReader(ms, Encoding.UTF8))
                    {
                        string jsonstring = await reader.ReadToEndAsync();
                        var details = JObject.Parse(jsonstring);

                        if (details["msg_type"].ToString() == "notify_state_change")
                        {
                            Console.WriteLine(details["data"]["id"]);

                        }

                    }
                }
            } while (true);
        }
    }
}
