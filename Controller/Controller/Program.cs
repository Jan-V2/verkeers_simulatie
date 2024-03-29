﻿using System;
using System.IO;
using System.Text;
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
        //Global variables
        static int message_id = 0;
        static string cycle_state = "red";
        static bool cycle_state_fresh = true;
        static List<Sensor> sensors = new List<Sensor>();
        static List<int> currentWorkingLights = new List<int>();
        static List<TrafficLight> trafficLights = new List<TrafficLight>();
        static long cycle_state_time = DateTimeOffset.Now.ToUnixTimeSeconds();

        //Main program
        static async Task Main(string[] args)
        {
            string ip = "ws://127.0.0.1:6969"; //Starts with local ip
            do
            {
                using (var socket = new ClientWebSocket())
                    try
                    {
                        //Make socket connection
                        await socket.ConnectAsync(new Uri(ip), CancellationToken.None);
                        Console.WriteLine("Connected");

                        //Start receive loop
                        Receive(socket);
                        Thread.Sleep(500);

                        //Start main loop
                        Stopwatch sw = new Stopwatch();
                        while (true)
                        {
                            sw.Start();
                            {
                                //Cleanup from previously "greened" traffic lights
                                foreach (TrafficLight tl in trafficLights)
                                {
                                    if (tl.state == "green" && CurrentTime() - tl.statechangetime > 10)
                                    {
                                        tl.state = "orange";
                                        tl.statechangetime = CurrentTime();
                                    }
                                    else if (tl.state == "orange" && CurrentTime() - tl.statechangetime > 4)
                                    {
                                        tl.state = "red";
                                        tl.statechangetime = CurrentTime();
                                    }
                                    else if (tl.state == "red" && CurrentTime() - tl.statechangetime > tl.clearing_time)
                                    {
                                        currentWorkingLights.Remove(tl.id);
                                    }
                                }

                                //For all busses, try greening them
                                foreach (Sensor sensor in sensors)
                                {
                                    if (sensor.public_transport && evaluate_trafficlight_compatibility(sensor.id, currentWorkingLights) && !currentWorkingLights.Contains(sensor.id))
                                    {
                                        TrafficLight tl = TrafficLightByID(sensor.id);
                                        tl.state = "green";
                                        tl.statechangetime = CurrentTime();
                                        tl.Touch();
                                        currentWorkingLights.Add(sensor.id);
                                    }
                                }

                                //For all trafficlights who haven't been "greened" for longer than a minute
                                List<int> blacklist = new List<int>();
                                List<int> longerthanninety = new List<int>();
                                {
                                    List<int> waiting_for_long = new List<int>();
                                    List<long> time = new List<long>();

                                    //Make list of traffic lights that haven't been greened for longer than 90s
                                    foreach(TrafficLight tl in trafficLights)
                                    {
                                        if(CurrentTime() - tl.lastupdated > 90)
                                        {
                                            longerthanninety.Add(tl.id);
                                        }
                                    }

                                    //All trafficlights that haven't been greened for over 60s get priority and lights that haven't been greened get all crossings blacklisted
                                    foreach (TrafficLight tl in trafficLights)
                                    {
                                        if (CurrentTime() - tl.lastupdated > 60)
                                        {
                                            waiting_for_long.Add(tl.id);
                                            time.Add(CurrentTime() - tl.lastupdated);
                                            if(CurrentTime() - tl.lastupdated > 90)
                                            {
                                                foreach(int bl in tl.crosses)
                                                {
                                                    if (!blacklist.Contains(bl) && !longerthanninety.Contains(bl)) blacklist.Add(bl);
                                                }
                                            }
                                        }
                                    }

                                    //Sort the list of long waiting trafficlights by amount of negligence
                                    int index = 0;
                                    while (waiting_for_long.Count >= 2)
                                    {
                                        if (index == waiting_for_long.Count - 1) break;
                                        if (time[index] < time[index + 1])
                                        {
                                            int waitingtemp = waiting_for_long[index + 1];
                                            long timetemp = time[index + 1];
                                            waiting_for_long.RemoveAt(index + 1);
                                            time.RemoveAt(index + 1);
                                            waiting_for_long.Insert(index, waitingtemp);
                                            time.Insert(index, timetemp);
                                            index = 0;
                                            continue;
                                        }
                                        index++;
                                    }

                                    //Green trafficlights that have waited for longer than 60s in order of negligence amount
                                    foreach (int id in waiting_for_long)
                                    {
                                        if (evaluate_trafficlight_compatibility(id, currentWorkingLights) && !currentWorkingLights.Contains(id) && !blacklist.Contains(id))
                                        {
                                            TrafficLight tl = TrafficLightByID(id);
                                            tl.state = "green";
                                            tl.statechangetime = CurrentTime();
                                            tl.Touch();
                                            currentWorkingLights.Add(id);
                                        }
                                    }
                                }

                                //Finally add trafficlights with active sensors
                                foreach (Sensor sensor in sensors)
                                {
                                    if (!sensor.vehicles_blocking && (sensor.vehicles_waiting || sensor.vehicles_coming) && evaluate_trafficlight_compatibility(sensor.id, currentWorkingLights) && !currentWorkingLights.Contains(sensor.id) && !blacklist.Contains(sensor.id))
                                    {
                                        TrafficLight tl = TrafficLightByID(sensor.id);
                                        tl.state = "green";
                                        tl.statechangetime = CurrentTime();
                                        tl.Touch();
                                        currentWorkingLights.Add(sensor.id);
                                    }
                                }

                                //Send json message to simulation with all traffic lights
                                message_id++;
                                string jsonstring = "{\"msg_id\": " + message_id + ", \"msg_type\": \"notify_traffic_light_change\", \"data\": [";
                                for (int c = 0; c < trafficLights.Count; c++)
                                {
                                    jsonstring = jsonstring + "{\"id\": " + trafficLights[c].id + ", \"state\": \"" + trafficLights[c].state + "\"" + "}";
                                    if ((c + 1) != trafficLights.Count)
                                        jsonstring = jsonstring + ", ";
                                }
                                jsonstring = jsonstring + "]}";
                                await Send(socket, jsonstring);
                            }

                            //Sleep for some additional time, so that one message is sent per second
                            sw.Stop();
                            if (sw.ElapsedMilliseconds < 1000)
                                Thread.Sleep(1000 - (int)sw.ElapsedMilliseconds);
                            sw.Reset();
                        }
                    }
                    //Shows any error and asks for a new ip if the user wants to change it
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

        //Sends a given message and prints useful information to the console
        static async Task Send(ClientWebSocket socket, string data)
        {
            await socket.SendAsync(Encoding.UTF8.GetBytes(data), WebSocketMessageType.Text, true, CancellationToken.None);
            var details = JObject.Parse(data);
            Console.WriteLine("<- | MSG #" + details["msg_id"] + ", Type: " + details["msg_type"]);
        }

        //Starts a receive loop for receiving messages from the simulation and prints useful information to the console
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

                        //Gets message type and acts accordingly
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
                                    int id = sensor["id"].ToObject<int>();
                                    if (sensor["vehicles_waiting"] != null)
                                    {
                                        ChangeSensor(id, "waiting", sensor["vehicles_waiting"].ToObject<bool>());
                                    }
                                    if (sensor["vehicles_coming"] != null)
                                    {
                                        ChangeSensor(id, "coming", sensor["vehicles_coming"].ToObject<bool>());
                                    }
                                    if (sensor["vehicles_blocking"] != null)
                                    {
                                        ChangeSensor(id, "blocking", sensor["vehicles_blocking"].ToObject<bool>());
                                    }
                                    if (sensor["emergency_vehicle"] != null)
                                    {
                                        ChangeSensor(id, "emergency", sensor["emergency_vehicle"].ToObject<bool>());
                                    }
                                    if (sensor["public_vehicle"] != null)
                                    {
                                        ChangeSensor(id, "public", sensor["public_vehicle"].ToObject<bool>());
                                    }
                                }
                                break;
                        }
                    }
                }
            } while (true);
        }

        //Checks whether a traffic light ID has a corresponding sensor
        static bool SensorExists(int sensorid)
        {
            foreach (Sensor sensor in sensors)
                if (sensor.id == sensorid)
                    return true;
            return false;
        }

        //Changes the value of a sensor flag
        static void ChangeSensor(int sensorid, string flagtype, bool value)
        {
            foreach (Sensor sensor in sensors)
            {
                if (sensor.id == sensorid)
                {
                    switch (flagtype)
                    {
                        case "waiting":
                            sensor.vehicles_waiting = value;
                            break;
                        case "coming":
                            sensor.vehicles_coming = value;
                            break;
                        case "blocking":
                            sensor.vehicles_blocking = value;
                            break;
                        case "emergency":
                            sensor.emergency_vehicle = value;
                            break;
                        case "public":
                            sensor.public_transport = value;
                            break;
                    }
                }
            }
        }

        //Gives the current time more neatly
        static long CurrentTime()
        {
            return DateTimeOffset.Now.ToUnixTimeSeconds();
        }

        //Returns a TrafficLight object from the list of existing traffic lights by id
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

        //Evaluates if a traffic light ID is compatible with the currently (or recently) active traffic lights 
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

        //Cleans up after a disconnect so that the controller is reuseable
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

    //TrafficLight class for storing data
    class TrafficLight
    {
        public int id;
        public List<int> crosses;
        public double clearing_time;
        public string state;
        public long lastupdated;
        public long statechangetime;
        public TrafficLight(int id, List<int> crosses, double clearing_time)
        {
            this.id = id;
            this.crosses = crosses;
            this.clearing_time = clearing_time;
            lastupdated = DateTimeOffset.Now.ToUnixTimeSeconds();
            statechangetime = DateTimeOffset.Now.ToUnixTimeSeconds();
            state = "red";
        }

        public void Touch()
        {
            lastupdated = DateTimeOffset.Now.ToUnixTimeSeconds();
        }
    }

    //Sensor class for storing data
    class Sensor
    {
        public int id;
        public bool vehicles_waiting;
        public bool vehicles_coming;
        public bool vehicles_blocking;
        public bool emergency_vehicle;
        public bool public_transport;

        public Sensor(int id)
        {
            this.id = id;
            this.vehicles_waiting = false;
            this.vehicles_coming = false;
            this.vehicles_blocking = false;
            this.emergency_vehicle = false;
            this.public_transport = false;
        }
    }
}
