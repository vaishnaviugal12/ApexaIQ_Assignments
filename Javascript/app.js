let gameseq = [];
let userseq = [];
let btns = ["red","blue","green","pink"];

let started = false;
let level = 0;
let score = 0;

let h3 = document.querySelector("h3");

// Start game
document.addEventListener("keypress", function(){
    if(!started){
        console.log("Game started!");
        started = true;
        level = 0;
        gameseq = [];
        levelup();
    }
});

function gameflash(btn){
    btn.classList.add("flash");
    setTimeout(() => btn.classList.remove("flash"), 300);
}
function userflash(btn){
    btn.classList.add("userflash");
    setTimeout(() => btn.classList.remove("userflash"), 300);
}

function levelup(){
    userseq = [];
    level++;
    h3.innerText = `Level ${level}`;

    let randidx = Math.floor(Math.random() * btns.length); // FIXED
    let randcolor = btns[randidx];
    let randbtn = document.querySelector(`.${randcolor}`);
    gameseq.push(randcolor);
    console.log("Game sequence:", gameseq);
    gameflash(randbtn);
}

function checkAns(idx){
    if(userseq[idx] === gameseq[idx]){
        if(userseq.length === gameseq.length){
            setTimeout(levelup, 1000);
        }
    } else {
        h3.innerHTML = `Game Over! Your score was <b>${level}</b><br>Press any key to restart`;
        document.body.style.backgroundColor = "red";
        setTimeout(() => document.body.style.backgroundColor="white", 200);

        reset();
    }
}

function btnpress(){
    let btn = this;
    userflash(btn);
    let usercolor = btn.getAttribute("id");
    userseq.push(usercolor);
    checkAns(userseq.length-1);
}

let allbtns = document.querySelectorAll(".btn");
for(let btn of allbtns){
    btn.addEventListener("click", btnpress);
}

function reset(){
    if(level > score){
        score = level;
    }
    document.querySelector("h2").innerHTML = `Highest Score: <b>${score}</b>`;
    
    started = false;
    gameseq = [];
    userseq = [];
    level = 0;
}
