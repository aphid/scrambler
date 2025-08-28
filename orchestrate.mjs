import * as fs from 'fs';
//import * as exec from 'exec';

let sourceDir = "/home/aphid/projects/numb_station/scram/"

let files = fs.readdirSync(sourceDir);
for (let i = 0; i < files.length; i++){
  files[i] = sourceDir + files[i];
  console.log(files[i]);
}
let left = subset(files);
let right = subset(files);
let data = {left: left, right: right};
console.log(data);
fs.writeFileSync("numbers.json", JSON.stringify(data, undefined, 2));


function subset(array){
  let arr = shuffleArray(array);
  let size = randomInt(5,23) - 1;
  return arr.slice(0,size)
}


function randomInt(min, max) {
  const minCeiled = Math.ceil(min);
  const maxFloored = Math.floor(max);
  return Math.floor(Math.random() * (maxFloored - minCeiled) + minCeiled); // The maximum is exclusive and the minimum is inclusive
}



function shuffleArray(array) {
  let currentIndex = array.length, randomIndex;

  // While there remain elements to shuffle.
  while (currentIndex !== 0) {

    // Pick a remaining element.
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex--;

    // And swap it with the current element.
    [array[currentIndex], array[randomIndex]] = [
      array[randomIndex], array[currentIndex]];
  }

  return array;
}
