targetDemo = '';

fetch('/loadApps',{method:'POST'})
.then(res=>res.json())
.then((data)=>{
    if (data.msg == "success"){
        arrApps = data.lsapps.split("///");
        arrApps.pop();
        pog=1;
        tmpActive="";
        arrApps.forEach(element => {
            itsName = element.split("&&&")[0];
            itsRoute = element.split("&&&")[1];
            itsDesc = element.split("&&&")[2];
            if (pog == 1){
                tmpActive="u-active";
            }
            if (pog != 1){
                tmpActive="";
            }
            templa00 =`
                <div class="${tmpActive} u-align-center u-carousel-item u-container-style u-palette-5-light-1 u-slide">
                    <div class="u-container-layout u-container-layout-${pog}">
                        <img alt="" class="u-image u-image-default u-image-${pog}" data-image-width="521" data-image-height="417" src="/imgApp/${itsName}">
                        <p class="u-align-left u-text u-text-default u-text-${pog+2}">${itsDesc}</p>
                        <table style="position:absolute;bottom:10px;right:0;">
                        <tr>
                        <td>
                        <a onclick="targetDemo ='${itsName}';window.scrollTo(0,0);openNavX();" class="u-btn u-btn-round u-button-style u-hover-palette-1-light-1 u-palette-1-base u-radius-50 u-btn-1">▷ DEMO</a>
                        </td>
                        <td>
                        <a href="${itsRoute}" class="u-btn u-btn-round u-button-style u-hover-palette-1-light-1 u-palette-1-base u-radius-50 u-btn-1">ACCÉDER</a>
                        </td>
                        </tr>
                        </table>
                    </div>
                </div>
            `;
            document.querySelector('#AllTheApps').innerHTML += templa00;
            pog++;
        });
    }
    if (data.msg == "empty"){
        document.getElementById('maintenaceModal').style.display = 'block';
    }
})
.catch((e)=>{console.log(e);});



function openNavX() {
    document.getElementById("myNavX").style.width = "100%";
    console.log(targetDemo);
    
    videoEl = document.getElementById('videoplace');
    fetch("/demApp/"+targetDemo.toString())
    .then(res=>res.blob())
    .then((videoFile)=>{
        videoUrl=window.URL.createObjectURL(videoFile);// blob.data gives actual data
        videoEl.src = videoUrl;
    }).catch(e=>console.log(e));
}  
function closeNavX() {
    document.getElementById("myNavX").style.width = "0%";
}

