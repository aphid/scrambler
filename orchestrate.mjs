import * as fs from 'fs';
import * as cp from 'child_process';

const freq = "90.6";

let leftDir = "../conet/";
let rightDir = "../common/";
let leftF = fs.readdirSync(leftDir);
for (let i = 0; i < leftF.length; i++){
  leftF[i] = leftDir + leftF[i];
}

let rightF = fs.readdirSync(rightDir);
console.log("........",rightF.length);
for (let i = 0; i < rightF.length; i++){
  console.log("adding");
  rightF[i] = rightDir + rightF[i];
}

function select(){
   let left = subset(leftF);
   let right = subset(rightF);
   let data = {left: left, right: right};
    fs.writeFileSync("numbers.json", JSON.stringify(data, undefined, 2));
}


let cycle = async function(){
   console.log("broadcasting");
   broadcast();
   console.log("they live, we sleep");
   await sleep(5000);
   console.log("selecting");
   select();
   console.log("arranging");
   await concat();
   console.log("making stereo file");
   await join();
   //ffmpeg -i input_left.mp3 -i input_right.mp3 -filter_complex "[0:a][1:a]amerge=inputs=2[a]" -map "[a]" output.mp3
}

function sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
}
select();
await concat();
await join();
broadcast();

async function broadcast(){
    let cmd = `/home/aphid/fm_transmitter/fm_transmitter`;
    let args = [`-f`, `${freq}`, `/home/aphid/scrambler/stereo.wav`];
    return new Promise(async (resolve)=>{
        try {
            console.log(cmd);
            let child = cp.spawn('sudo', [cmd, ...args]);
            child.on('close', async (code) => {
		console.log("broadcast is done, onto the next");
                return await broadcast();
            });
	    console.log("sleeping");
	    await sleep(5000);
	    console.log("selecting");
	    select();
	    console.log("concatenating");
	    await concat();
	    console.log("making stereo");
	    await join();
	    
        } catch (e) {
            console.error(e);
        }
    });
}

async function concat(){
    let cmd = `"/home/aphid/scrambler/.scramblr/bin/python3" "/home/aphid/scrambler/concat.py"`;
    try {
        console.log(cmd);
        let thecmd = cp.execSync(cmd).toString();
        console.log(thecmd);
	return Promise.resolve();
    } catch (e) {
        console.error(e);
    }
}

async function join(){
let cmd = `ffmpeg -i left.wav -i right.wav -filter_complex "[0:a][1:a]amerge=inputs=2[a]" -map "[a]" -y -f wav -bitexact -acodec pcm_s16le -ar
 22050 stereo.wav`;
    console.log(cmd);
    try {
        let doTheThing = cp.execSync(cmd).toString();
        console.log(doTheThing);
        if (doTheThing.includes("nothing was encoded")) {
            process.exit();
        }
	return Promise.resolve();
    } catch (e) {
        throw (e);
    }
}

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
