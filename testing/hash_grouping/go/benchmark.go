package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"time"
	"flag"
	"strings"
)

func filter(arr []Course, valid []string) []Course {
	result := []Course{}
	for i := range arr {
		for j := range valid {
			if arr[i].Name == valid[j] {
				result = append(result, arr[i])
			}
		}
	}
	return result
}

func main() {
	term := flag.Int("term", -1,"Term to create schedules for")
	names := flag.String("courses", "", "List of courses to create schedules from")
	flag.Parse()
	course_names := strings.Split(*names, ",")
	path := fmt.Sprintf("table-%v.json", *term)

	content, err := ioutil.ReadFile(path)
	if err != nil {
		log.Fatal(err)
	}

	var data []Course
	err = json.Unmarshal(content, &data)
	if err != nil {
		log.Fatal(err)
	}
	
	courses := filter(data, course_names)

	start := time.Now()
	results := CreateSchedules(courses)
	duration := time.Since(start).Seconds()

	fmt.Printf("duration: %.2f seconds\n", duration)
	fmt.Println("count: ", len(results))
}
