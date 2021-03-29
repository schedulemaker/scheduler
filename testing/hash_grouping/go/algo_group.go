package main

type Availability struct {
	Count     int
	Capacity  int
	Available int
}

type Location struct {
	Building string
	Room     string
}

type Instructor struct {
	Id   int
	Name string
}

type Crn struct {
	Crn         int
	Campus      string
	Section     string
	Instructors []Instructor
	Locations   []Location
	Enrollment  Availability
	Waitlist    Availability
}

type Classtime struct {
	Start_time int
	End_time   int
	Days       int
	Start_date int
	End_date   int
}

type CourseGroup struct {
	Hash       string
	Classtimes []Classtime
	Crns       []Crn
}

type Course struct {
	Name   string
	Title  string
	Groups []CourseGroup
}

// func peek[T any](stack []T) T {
// 	return stack[len(stack) - 1]
// }

func check_times(to_check []Classtime, schedule []Classtime) bool {
	for i := range to_check {
		classtime_a := to_check[i]
		for j := range schedule {
			classtime_b := schedule[j]
			if !(classtime_a.Start_time > classtime_b.End_time || classtime_b.Start_time > classtime_a.End_time){
				if (classtime_a.Days & classtime_b.Days) != 0 {
					if !(classtime_a.Start_date > classtime_b.End_date || classtime_b.Start_date > classtime_a.End_date){
						return false
					}
				}
			}
		}
	}
	return true
}

func CreateSchedules(courses []Course) [][]CourseGroup{
	first := courses[0].Groups[0]
	group_idxs, temp, temp_classtimes, results := []int{1}, []CourseGroup{first}, [][]Classtime{first.Classtimes}, [][]CourseGroup{}
	course_idx, group_idx := 0, -1

	for course_idx >= 0 {
		if course_idx+1 != len(temp) {
			group_idx = group_idxs[len(group_idxs)-1]
			group_idxs = group_idxs[:len(group_idxs)-1]
		} else {
			course_idx++
			group_idx = 0
		}

		current_course := courses[course_idx].Groups
		for group_idx < len(current_course) {
			group := current_course[group_idx]
			if len(temp) == 0 || len(group.Classtimes) == 0 || check_times(group.Classtimes, temp_classtimes[len(temp_classtimes)-1]) {
				temp = append(temp, group)
				if len(temp_classtimes) == 0 {
					temp_classtimes = append(temp_classtimes, group.Classtimes)
				} else {
					temp_classtimes = append(temp_classtimes, temp_classtimes[len(temp_classtimes)-1])
					temp_classtimes[len(temp_classtimes)-1] = append(temp_classtimes[len(temp_classtimes)-1], group.Classtimes...)
				}
				group_idxs = append(group_idxs, group_idx+1)
				break
			} else {
				group_idx++
			}
		}

		if len(temp) == len(courses) {
			results = append(results, temp)
			temp = temp[:len(temp)-1]
			temp_classtimes = temp_classtimes[:len(temp_classtimes)-1]
		} else if group_idx >= len(current_course) {
			if course_idx > 0 {
				temp = temp[:len(temp)-1]
				temp_classtimes = temp_classtimes[:len(temp_classtimes)-1]
			}
			course_idx--
		} else {
		}
	}
	return results
}
