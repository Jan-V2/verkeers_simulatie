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
        static int message_id = 0;
        static List<TrafficLight> trafficLights = new List<TrafficLight>();
        static List<Sensor> sensors = new List<Sensor>();
        static List<int> currentWorkingLights = new List<int>();
        static long cycle_state_time = DateTimeOffset.Now.ToUnixTimeSeconds();
        static string cycle_state = "red";
        static bool cycle_state_fresh = true;

        static bool debug = false;

        static async Task Main(string[] args)
        {
            string ip = "ws://127.0.0.1:6969";
            do
            {
                using (var socket = new ClientWebSocket())
                    try
                    {
                        await socket.ConnectAsync(new Uri(ip), CancellationToken.None);
                        Console.WriteLine("Connected");
                        //await Send(socket, "data");
                        Receive(socket);
                        Thread.Sleep(500);
                        Stopwatch sw = new Stopwatch();
                        //bool tlcolor = true;
                        while (true)
                        {
                            //Voer dit uit aan het begin van de loop
                            sw.Start();

                            {
                                /*while (true)
                                {
                                    message_id++;
                                    await Send(socket, "{\"msg_id\": " + message_id.ToString() + ", \"msg_type\": \"test\", \"data\": [1, 2]}");
                                    Console.WriteLine(socket.State.ToString());
                                    Thread.Sleep(2000);
                                }*/
                                string jsonstring;
                                switch (cycle_state)
                                {
                                    case "red":
                                        cycle_state = "green";
                                        currentWorkingLights.Clear();
                                        cycle_state_time = CurrentTime();
                                        cycle_state_fresh = true;
                                        /*message_id++;
                                        jsonstring = "{\"msg_id\": " + message_id + ", \"msg_type\": \"notify_traffic_light_state\", \"data\": [";
                                        for (int c = 0; c < trafficLights.Count; c++)
                                        {
                                            jsonstring = jsonstring + "{\"id\": " + trafficLights[c].id + ", \"state\": \"red\"}";
                                            if ((c + 1) != trafficLights.Count)
                                                jsonstring = jsonstring + ", ";
                                        }
                                        jsonstring = jsonstring + "]}";
                                        await Send(socket, jsonstring);*/
                                        break;
                                    case "orange":
                                        double longest_clearing_time = 0;
                                        foreach (int i in currentWorkingLights)
                                            if (TrafficLightByID(i).clearing_time > longest_clearing_time)
                                                longest_clearing_time = TrafficLightByID(i).clearing_time;

                                        if (cycle_state_fresh)
                                        {
                                            message_id++;
                                            jsonstring = "{\"msg_id\": " + message_id + ", \"msg_type\": \"notify_traffic_light_change\", \"data\": [";
                                            for (int c = 0; c < trafficLights.Count; c++)
                                            {
                                                jsonstring = jsonstring + "{\"id\": " + trafficLights[c].id + ", \"state\": " + (currentWorkingLights.Contains(trafficLights[c].id) ? "\"orange\"" : "\"red\"") + "}";
                                                if ((c + 1) != trafficLights.Count)
                                                    jsonstring = jsonstring + ", ";
                                            }
                                            jsonstring = jsonstring + "]}";
                                            await Send(socket, jsonstring);
                                            cycle_state_fresh = false;
                                        }else if((CurrentTime() - cycle_state_time) > longest_clearing_time)
                                        {
                                            cycle_state = "red";
                                            cycle_state_fresh = true;
                                            cycle_state_time = CurrentTime();
                                        }
                                        break;
                                    case "green":
                                        if(cycle_state_fresh)
                                        {
                                            int oldestid = 1;
                                            long longesttimesinceupdate = 0;
                                            foreach (TrafficLight tl in trafficLights)
                                                if ((CurrentTime() - tl.lastupdated) >= longesttimesinceupdate)
                                                {
                                                    oldestid = tl.id;
                                                    longesttimesinceupdate = (CurrentTime() - tl.lastupdated);
                                                }
                                            if(debug)
                                                Console.WriteLine("Longest waiting time: " + longesttimesinceupdate);

                                            currentWorkingLights.Add(oldestid);

                                            foreach (Sensor sensor in sensors)
                                                if (sensor.isOn)
                                                    if (!currentWorkingLights.Contains(sensor.id) && evaluate_trafficlight_compatibility(sensor.id, currentWorkingLights))
                                                        currentWorkingLights.Add(sensor.id);

                                            foreach (TrafficLight tl in trafficLights)
                                                if (!currentWorkingLights.Contains(tl.id) && evaluate_trafficlight_compatibility(tl.id, currentWorkingLights))
                                                    currentWorkingLights.Add(tl.id);

                                            foreach (TrafficLight tl in trafficLights)
                                                if (currentWorkingLights.Contains(tl.id))
                                                    tl.Touch();
                                            cycle_state_fresh = false;
                                            message_id++;
                                            jsonstring = "{\"msg_id\": " + message_id + ", \"msg_type\": \"notify_traffic_light_change\", \"data\": [";
                                            for (int c = 0; c < trafficLights.Count; c++)
                                            {
                                                jsonstring = jsonstring + "{\"id\": " + trafficLights[c].id + ", \"state\": " + (currentWorkingLights.Contains(trafficLights[c].id) ? "\"green\"" : "\"red\"") + "}";
                                                if ((c + 1) != trafficLights.Count)
                                                    jsonstring = jsonstring + ", ";
                                            }
                                            jsonstring = jsonstring + "]}";
                                            await Send(socket, jsonstring);
                                        }
                                        else if((CurrentTime() - cycle_state_time) >  10)
                                        {
                                            cycle_state = "orange";
                                            cycle_state_fresh = true;
                                            cycle_state_time = CurrentTime();
                                        }
                                        break;
                                }
                            }

                            //Voer dit uit aan het einde van de loop
                            sw.Stop();
                            if (sw.ElapsedMilliseconds < 1000)
                                Thread.Sleep(1000 - (int)sw.ElapsedMilliseconds);
                            //Console.WriteLine("Current cycle state: " + cycle_state + ", fresh: " + cycle_state_fresh + ", duration of state right now: " + (CurrentTime() - cycle_state_time) + " seconds.");
                        }
                    }
                    catch (Exception ex)
                    {
                        Console.WriteLine($"ERROR - {ex.Message}");
                        Console.Write("Could not connect or something went wrong, type new ip or [Enter] for the same ip: ");
                        string input = Console.ReadLine();
                        if (input != "")
                            ip = "ws://" + input + ":6969";
                        CleanUp();
                    }
            } while (true);
        }

        static async Task Send(ClientWebSocket socket, string data)
        {
            await socket.SendAsync(Encoding.UTF8.GetBytes(data), WebSocketMessageType.Text, true, CancellationToken.None);
            //Console.WriteLine(data);
            //Console.WriteLine(socket.State.ToString());
            var details = JObject.Parse(data);
            Console.WriteLine("<- | MSG #" + details["msg_id"] + ", Type: " + details["msg_type"]);
        }

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

                        message_id = details["msg_id"].ToObject<int>();
                        
                        Console.WriteLine("-> | MSG #" + message_id + ", Type: " + details["msg_type"]);

                        switch (details["msg_type"].ToString()){
                            case "initialization":
                                trafficLights.Clear();
                                foreach (var tl in details["data"])
                                {
                                    int a = tl["id"].ToObject<int>();
                                    List<int> b = tl["crosses"].ToObject<List<int>>();
                                    double c = tl["clearing_time"].ToObject<double>();
                                    trafficLights.Add(new TrafficLight(a, b, c));
                                }
                                break;
                            case "notify_sensor_change":
                                foreach(var sensor in details["data"])
                                {
                                    if (!SensorExists(sensor["id"].ToObject<int>()))
                                        sensors.Add(new Sensor(sensor["id"].ToObject<int>()));
                                    ChangeSensor(sensor["id"].ToObject<int>(), sensor["vehicles_coming"].ToObject<bool>() || sensor["vehicles_waiting"].ToObject<bool>());
                                }
                                break;
                        }
                    }
                }
            } while (true);
        }

        static bool SensorExists(int sensorid)
        {
            foreach (Sensor sensor in sensors)
                if (sensor.id == sensorid)
                    return true;

            return false;
        }
        
        static void ChangeSensor(int sensorid, bool state)
        {
            foreach (Sensor sensor in sensors)
                if (sensor.id == sensorid)
                    sensor.isOn = state;
        }

        static long CurrentTime()
        {
            return DateTimeOffset.Now.ToUnixTimeSeconds();
        }

        static TrafficLight TrafficLightByID(int id)
        {
            for(int c = 0; c < trafficLights.Count; c++)
            {
                if(trafficLights[c].id == id)
                {
                    return trafficLights[c];
                }
            }
            return new TrafficLight(746, new List<int>(), 746.0F);
        }

        static bool evaluate_trafficlight_compatibility(int newtl, List<int> currentlist)
        {
            foreach(int valID in currentlist)
            {
                if (TrafficLightByID(valID).crosses.Contains(newtl))
                {
                    return false;
                }
            }
            return true;
        }

        static void CleanUp()
        {
            message_id = 0;
            trafficLights.Clear();
            sensors.Clear();
            currentWorkingLights.Clear();
            cycle_state = "red";
            cycle_state_fresh = true;
        }
    }

    class TrafficLight
    {
        public int id;
        public List<int> crosses;
        public double clearing_time;
        public string state;
        public long lastupdated;
        public TrafficLight(int id, List<int> crosses, double clearing_time)
        {
            this.id = id;
            this.crosses = crosses;
            this.clearing_time = clearing_time;
            lastupdated = DateTimeOffset.Now.ToUnixTimeSeconds();
            state = "red";
        }

        public void Touch()
        {
            lastupdated = DateTimeOffset.Now.ToUnixTimeSeconds();
        }
    }
    
    class Sensor
    {
        public int id;
        public bool isOn;

        public Sensor(int id)
        {
            this.id = id;
            this.isOn = false;
        }
    }
}
