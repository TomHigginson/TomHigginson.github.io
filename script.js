const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

let interval = null;
console.log("If you can see this message, I hope you know what you are doing!!!!")
const doc_h1 = document.querySelectorAll("h1")
for (let i = 0 ; i <doc_h1.length; i++) {
  doc_h1[i].onmouseover = event => {
    let iteration = 0;

    clearInterval(interval);

    interval = setInterval(() => {
      event.target.innerText = event.target.innerText
        .split("")
        .map((letter, index) => {
          if(index < iteration) {
            return event.target.dataset.value[index];
          }

          return letters[Math.floor(Math.random() * 26)]
        })
        .join("");

      if(iteration >= event.target.dataset.value.length){
        clearInterval(interval);
      }

      iteration += 1 / 2.5;
    }, 20);
  }
}


// const doc = document.querySelectorAll("a")
// for (let i = 0; i < doc.length; i++) {
//   doc[i].onmouseover = event => {
//     let iteration = 0;

//     clearInterval(interval);

//     interval = setInterval(() => {
//       event.target.innerText = event.target.innerText
//         .split("")
//         .map((letter, index) => {
//           if(index < iteration) {
//             return event.target.dataset.value[index];
//           }

//           return letters[Math.floor(Math.random() * 26)]
//         })
//         .join("");

//       if(iteration >= event.target.dataset.value.length){
//         clearInterval(interval);
//       }

//       iteration += 1 / 3;
//     }, 30);
//   }
// }

