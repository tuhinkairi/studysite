window.onload=()=>{

const slider = document.getElementById('slider')
const btn_left = document.getElementById('left')
const btn_right = document.getElementById('right')
const imgs = document.getElementsByClassName('slider-img')
let record = imgs.length/2
let marker = 1
let list  = []
slider.style.transition = "1s";
btn_right.addEventListener('click', ()=>{
        
        data = marker%record 
        list.push(data)
        marker++;
        slider.style.transform = `translateX(${-100 * list[list.length-1]}%)`;
        console.log(marker,slider,list)
})
btn_left.addEventListener('click', ()=>{
        list.pop()
        if(list.length==''){
                for(let i =0; i<record ;i++ ){
                        list.push(i)
                        console.log(list,i)
                }
                marker = list.length 
        }
        console.log(marker,list)
        slider.style.transform = `translateX(${-100 * list[list.length-1]}%)`;    
})
}