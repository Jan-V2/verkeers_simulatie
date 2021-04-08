using System;
using System.IO;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Net.WebSockets;
using System.Threading;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;
using System.Diagnostics;
using System.Collections.Generic;

namespace Controller
{
    class Program
    {
        static async Task Main(string[] args)
        {
            string ip = "ws://127.0.0.1:6969";
            do
            {
                using (var socket = new ClientWebSocket())
                    try
                    {
                        await socket.ConnectAsync(new Uri(ip), CancellationToken.None);
                        Console.WriteLine("connected");
                        //await Send(socket, "data");
                        Receive(socket);
                        Stopwatch sw = new Stopwatch();
                        bool tlcolor = true;
                        while (true)
                        {
                            sw.Start(); //Voer dit uit aan het begin van de loop

                            await Send(socket, "{\"msg_id\": 0, \"msg_type\": \"perform_change_state\", \"data\": [{\"id\": 0, \"state\":" + (tlcolor ? "\"green\"" : "\"red\"") + "}]}");
                            tlcolor = !tlcolor;

                            //Voer dit uit aan het einde van de loop
                            sw.Stop();
                            if (sw.ElapsedMilliseconds < 1000)
                                Thread.Sleep(1000 - (int)sw.ElapsedMilliseconds);
                        }
                        

                    }
                    catch (Exception ex)
                    {
                        Console.WriteLine($"ERROR - {ex.Message}");
                        Console.Write("Could not connect or something went wrong, type new ip or [Enter] for the same ip: ");
                        string input = Console.ReadLine();
                        if (input != "")
                            ip = "ws://" + input + ":6969";
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

                        Console.Write("MSG #" + details["msg_id"].ToString() + " - ");

                        if (details["msg_type"].ToString() == "notify_state_change")
                        {
                            Console.WriteLine("Received traffic light #" + details["data"][0]["id"].ToString() + " with clearing time of " + details["data"][0]["clearing_time"] + ".");

                        }

                    }
                }
            } while (true);
        }
    }
}
