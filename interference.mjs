import * as fs from 'fs';
import * as cp from 'child_process';
import * as path from 'path'
const freq = 95.3;


let ifs = ["drs", "anna", "drs", "ejt", "fabiola", "mem", "rp", "sarashaw"];

let chorus = [];

for (let ifz of ifs){
    let files = fs.readdirSync("../interference/" + ifz + "/");
    for (let i = 0; i < files.length; i++){
        files[i] = "../interference/" + ifz + "/" + files[i];
    }
    chorus.push(...files);
}




function select(){
    
    fs.writeFileSync("numbers.json", JSON.stringify(subset(chorus), undefined, 2));
}


let cycle = async function(){
   console.log("broadcasting");
   await sleep(randomInt(17,31) * 1000);
   console.log("begin");
   broadcast();
   console.log("they live, we sleep");
   await sleep(5000);
   console.log("selecting");
   select();
   console.log("arranging");
   await concat();
   console.log("making stereo file");
   //await join();
   //ffmpeg -i input_left.mp3 -i input_right.mp3 -filter_complex "[0:a][1:a]amerge=inputs=2[a]" -map "[a]" output.mp3
}

function sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
}
select();
await concat();
//await join();
broadcast();

function tweakFreq(){
  let ch = randomInt(-25,25) * 0.01;
  return (freq + ch).toFixed(3);
  
}

async function broadcast(){
    let fq = tweakFreq();
    console.log("target freq: ", fq);
    //let cmd = `/home/aphid/fm_transmitter/fm_transmitter`;
    let cmd = `/home/aphid/PiFmRds/src/pi_fm_rds`;
    //let args = [`-f`, `${fq}`, `/home/aphid/scrambler/interfere.wav`];
    let args = [`-freq`, `${freq}`, `-audio`, `/home/aphid/scrambler/interfere.wav`];
    return new Promise(async (resolve)=>{
        try {
            console.log(cmd);
            let child = cp.spawn('sudo', [cmd, ...args]);
            child.on('close', async (code) => {
		console.log("broadcast is done, onto the next");
		await sleep(randomInt(17,31) * 1000);
                return await broadcast();
            });
	    console.log("sleeping");
	    await sleep(5000);
	    console.log("selecting");
	    select();
	    console.log("concatenating");
	    await concat();
	    //console.log("making stereo");
	    //await join();
	    
        } catch (e) {
            console.error(e);
        }
    });
}

async function concat(){
    let cmd = `"/home/aphid/scrambler/.scramblr/bin/python3" "/home/aphid/scrambler/concat_interference.py"`;
    try {
        console.log(cmd);
        let thecmd = cp.execSync(cmd).toString();
        console.log(thecmd);
	return Promise.resolve();
    } catch (e) {
        console.error(e);
    }
}
/*
async function join(){
let cmd = `ffmpeg -i interfere.wav -y -f wav -bitexact -acodec pcm_s16le -ar 22050 interfere.wav`;
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
}*/

function subset(array){
  let arr = shuffleArray(array);
  let size = randomInt(7,11);
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

