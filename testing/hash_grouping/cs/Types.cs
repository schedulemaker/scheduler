using System.Collections.Generic;

namespace Scheduler
{
    public class Course 
    {
        public string Name {get; set;}
        public string Title {get; set;}
        public IEnumerable<CourseGroup> Groups {get; set;}

        public Course(string name, string title, IEnumerable<CourseGroup> groups){
            Name = name;
            Title = title;
            Groups = groups;
        }
    }

    public class CourseGroup
    {
        public string Hash {get; set;}
        public IEnumerable<Classtime> Classtimes {get; set;}
        public IEnumerable<CRN> Crns {get; set;}

        public CourseGroup(string hash, IEnumerable<Classtime> classtimes, IEnumerable<CRN> crns){
            Hash = hash;
            Classtimes = classtimes;
            Crns = crns;
        }
    }

    public class Classtime
    {
        public int Start_Time {get; set;}
        public int End_Time {get; set;}
        public int Days {get; set;}
        public int Start_Date {get; set;}
        public int End_Date {get; set;}

        public Classtime(int startTime, int endTime, int days, int startDate, int endDate){
            Start_Time = startTime;
            End_Time = endTime;
            Days = days;
            Start_Date = startDate;
            End_Date = endDate;
        }
    }

    public class CRN 
    {
        public int Crn {get; set;}
        public string Campus {get; set;}
        public string Section {get; set;}
        public IEnumerable<Instructor> Instructors {get; set;}
        public IEnumerable<Location> Locations {get; set;}
        public Availability Enrollment {get; set;}
        public Availability Waitlist {get; set;}

        public CRN(int crn, string campus, string section, IEnumerable<Instructor> instructors, IEnumerable<Location> locations, Availability enrollment, Availability waitlist)
        {
            Crn = crn;
            Campus = campus;
            Section = section;
            Instructors = instructors;
            Locations = locations;
            Enrollment = enrollment;
            Waitlist = waitlist;
        }
    }

    public class Instructor 
    {
        public int Id {get; set;}
        public string Name {get; set;}

        public Instructor(int id, string name){
            Id = id;
            Name = name;
        }
    }

    public class Location 
    {
        public string Building {get; set;}
        public string Room {get; set;}

        public Location(string building, string room){
            Building = building;
            Room = room;
        }
    }

    public class Availability 
    {
        public int Count {get; set;}
        public int Capacity {get; set;}
        public int Available {get; set;}

        public Availability(int count, int capacity, int available){
            Count = count;
            Capacity = capacity;
            Available = available;
        }
    }
}