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

// fetch('https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY')
//   .then(response => response.json())
//   .then(data => {
//     const mediaType = data.media_type;
//     const url = data.url;

//     if (mediaType === 'image') {
//       // Still image or gif: set as background
//       document.body.style.backgroundImage = `url(${url})`;
//       document.body.style.backgroundSize = 'cover';
//       document.body.style.backgroundPosition = 'center';
//       document.body.style.backgroundRepeat = 'no-repeat';
//     } else if (mediaType === 'video') {
//       // Video: create and insert iframe
//       const videoWrapper = document.createElement('div');
//       videoWrapper.style.position = 'fixed';
//       videoWrapper.style.top = 0;
//       videoWrapper.style.left = 0;
//       videoWrapper.style.width = '100%';
//       videoWrapper.style.height = '100%';
//       videoWrapper.style.zIndex = '-1';
//       videoWrapper.style.overflow = 'hidden';
//       videoWrapper.innerHTML = `
//         <iframe src="${url}?autoplay=1&mute=1&controls=0&loop=1"
//                 frameborder="0"
//                 allow="autoplay; fullscreen"
//                 style="width:100%; height:100%; object-fit:cover;">
//         </iframe>
//       `;
//       document.body.prepend(videoWrapper);
//       document.body.style.backgroundColor = '#000'; 
//     } else {
//       console.warn("Unsupported APOD media type:", mediaType);
//     }
//   })
//   .catch(error => console.error('Error fetching NASA APOD:', error));

