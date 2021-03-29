using System.Collections.Generic;
using System.Linq;

namespace Scheduler
{
    public class AlgoGroup
    {
        private static bool CheckTimes(IEnumerable<Classtime> toCheck, IEnumerable<Classtime> schedule)
        {
            foreach (var classtimeA in toCheck)
            {
                foreach (var classtimeB in schedule)
                {
                    if (!(classtimeA.Start_Time > classtimeB.End_Time || classtimeB.Start_Time > classtimeA.End_Time))
                    {
                        if ((classtimeA.Days & classtimeB.Days) != 0)
                        {
                            if (!(classtimeA.Start_Date > classtimeB.End_Date || classtimeB.Start_Date > classtimeA.End_Date))
                            {
                                return false;
                            }
                        }
                    }
                }
            }
            return true;
        }
        public static IEnumerable<IEnumerable<CourseGroup>> CreateSchedules(IEnumerable<Course> courses)
        {
            courses = courses.OrderBy(course => course.Groups.Count());
            var first = courses.First().Groups.First();
            var groupIdxs = new Stack<int>(new[] { 1 });
            var temp = new Stack<CourseGroup>(new[] { first });
            var tempClasstimes = new Stack<IEnumerable<Classtime>>(new[] { first.Classtimes });
            var results = new List<IEnumerable<CourseGroup>>();
            var courseIdx = 0;
            var groupIdx = -1;

            while (courseIdx >= 0)
            {
                if (courseIdx + 1 != temp.Count)
                {
                    groupIdx = groupIdxs.Pop();
                }
                else
                {
                    courseIdx++;
                    groupIdx = 0;
                }

                var currentCourse = courses.ElementAt(courseIdx).Groups;
                while (groupIdx < currentCourse.Count())
                {
                    var group = currentCourse.ElementAt(groupIdx);
                    if (temp.Count == 0 || group.Classtimes.Count() == 0 || CheckTimes(group.Classtimes, tempClasstimes.Peek()))
                    {
                        temp.Push(group);
                        if (tempClasstimes.Count == 0)
                        {
                            tempClasstimes.Push(group.Classtimes);
                        }
                        else
                        {
                            tempClasstimes.Push(tempClasstimes.Peek().Concat(group.Classtimes));
                        }
                        groupIdxs.Push(groupIdx + 1);
                        break;
                    }
                    else
                    {
                        groupIdx++;
                    }
                }

                if (temp.Count == courses.Count())
                {
                    results.Add(temp.ToList());
                    temp.Pop();
                    tempClasstimes.Pop();
                }
                else if (groupIdx >= currentCourse.Count())
                {
                    if (courseIdx > 0)
                    {
                        temp.Pop();
                        tempClasstimes.Pop();
                    }
                    courseIdx--;
                }
                else { }
            }

            return results;
        }
    }
}
