using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;

namespace Controller
{
    class Program
    {
        static void Main(string[] args)
        {
            Socket sck = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            string ip;
            int port;
            Console.Write("Ip: ");
            ip = Console.ReadLine();
            Console.Write("Port: ");
            port = Int32.Parse(Console.ReadLine());
            IPEndPoint endPoint = new IPEndPoint(IPAddress.Parse(ip), port);
            //Trying to make a connection
            while (true)
            {
                try 
                { 
                    sck.Connect(endPoint);
                    break;
                }
                catch
                {
                    Console.WriteLine("Connecting to simulation not succesful, try again? (y/n)");
                    string response = Console.ReadLine();
                    if (response != "y")
                    {
                        return;
                    }
                }
            }
            
            //Asking user if what to do
            while (true)
            {
                Console.Write("[Send], [Receive] or [Quit]: ");
                string command = Console.ReadLine();
                try
                {
                    switch (command)
                    {
                        case "Send":
                            Console.Write("Message: ");
                            string message = Console.ReadLine();
                            byte[] sendbuffer = Encoding.Default.GetBytes(message);
                            sck.Send(sendbuffer, 0, sendbuffer.Length, 0);
                            break;
                        case "Receive":
                            byte[] receivebuffer = new byte[255];
                            int receive = sck.Receive(receivebuffer, 0, receivebuffer.Length, 0);
                            Array.Resize(ref receivebuffer, receive);
                            Console.WriteLine("Received: " + Encoding.Default.GetString(receivebuffer));
                            break;
                        case "Quit":
                            return;
                            break;
                    }
                    Console.WriteLine("Succesful");
                }
                catch
                {
                    Console.WriteLine("Unsuccesful");
                }
            }
        }
    }
}
