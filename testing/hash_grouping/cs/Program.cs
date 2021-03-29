using System;
using System.IO;
using Newtonsoft.Json;
using System.Collections.Generic;
using System.Linq;
using System.Diagnostics;
using CommandLine;

namespace Scheduler
{
    class Program
    {
        public class Options
        {
            [Option("term", Required = true, HelpText = "Term to generate schedules for")]
            public int Term {get; set;}
            [Option("courses", Required = true, HelpText = "List of courses to generate schedules from")]
            public IEnumerable<string> Courses {get; set;}
        }
        static void Main(string[] args)
        {
            Parser.Default.ParseArguments<Options>(args)
                .WithParsed<Options>(o => {
                    var timer = new Stopwatch();
                    using (StreamReader r = File.OpenText($"../table-{o.Term}.json"))
                    {
                        string json = r.ReadToEnd();
                        var items = JsonConvert.DeserializeObject<IEnumerable<Course>>(json);
                        var courses = items.Where(item => o.Courses.Contains(item.Name));

                        timer.Start();
                        var results = AlgoGroup.CreateSchedules(courses);
                        timer.Stop();
                        var duration = timer.Elapsed;
                        Console.WriteLine($"Duration: {(float)duration.Seconds + (float)duration.Milliseconds / 1000} seconds");
                        Console.WriteLine($"Count: {results.Count()}");
                    }
                });  
        }
    }
}
