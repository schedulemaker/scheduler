const create_schedules = require('./algo_group');
const { program } = require('commander');
const fs = require('fs');

program
    .requiredOption('--term <term>', 'Term to create schedules for')
    .option('--log', 'Log results to a file')
    .requiredOption('--courses <courses...>', 'List of courses to create schedules from')

program.parse();
const options = program.opts();

const data = require(`../table-${options.term}.json`);
const courses = data.filter(c => options.courses.includes(c.name));

const start = process.hrtime();
let results = create_schedules(courses);
const end = process.hrtime(start);
const duration = end[0] + Number((end[1]/1e9).toFixed(2));

console.log(`duration: ${duration} seconds`);
console.log(`count: ${results.length}`);

if (options.log){
    results = results.map(result => result.map(g => g.hash).join(''));
    results.unshift({'algorithm': 'hash/group', 'duration': `${duration} seconds`, 'count': results.length});
    fs.writeFileSync(`results-${options.term}.js.json`, JSON.stringify(results, null, 2));
}