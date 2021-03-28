Array.prototype.peek = function(){
    return this[this.length - 1];
}

function check_times(to_check, schedule){
    for (const classtime_a of to_check){
        for (const classtime_b of schedule){
            if (!(
                classtime_a.start_time > classtime_b.end_time 
                || 
                classtime_b.start_time > classtime_a.end_time
            )){
                if (classtime_a.days & classtime_b.days){
                    if (!(
                        classtime_a.start_date > classtime_b.end_date
                        || 
                        classtime_b.start_date > classtime_a.end_date
                    )){
                        return false;
                    }
                }
            }
        }
    }
    return true;
}

function create_schedules(courses){
    courses.sort((a,b) => a.groups.length - b.groups.length);
    let first = courses[0].groups[0];
    let [group_idxs, temp, temp_classtimes, results] = [[1], [first], [first.classtimes], []];
    let course_idx = 0;
    let group_idx = -1;

    while (course_idx >= 0) {
        if (course_idx + 1 != temp.length){
            group_idx = group_idxs.pop();
        }
        else {
            course_idx++;
            group_idx = 0;
        }

        let current_course = courses[course_idx].groups;
        while (group_idx < current_course.length){
            let group = current_course[group_idx];
            if (temp.length == 0 || group.classtimes.length == 0 || check_times(group.classtimes, temp_classtimes.peek())){
                temp.push(group);
                if (temp_classtimes.length == 0){
                    temp_classtimes.push(group.classtimes);
                }
                else {
                    temp_classtimes.push([...temp_classtimes.peek(), ...group.classtimes]);
                }
                group_idxs.push(group_idx + 1);
                break;
            }
            else {
                group_idx++;
            }
        }

        if (temp.length == courses.length){
            results.push([...temp]);
            temp.pop();
            temp_classtimes.pop();
        }
        else if (group_idx >= current_course.length){
            if (course_idx > 0){
                temp.pop();
                temp_classtimes.pop();
            }
            course_idx--;
        }
        else {}
    }

    return results;
}

module.exports = create_schedules;