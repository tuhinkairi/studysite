// mini menu function
const menu = document.getElementById('mini-menu')
const menubtn = document.getElementById('minimenu-btn')
let condition = false

menubtn.addEventListener('click',()=>{
    menu.style.transition = '1s' 
    if(condition){
        menu.style.transform='translateY(-320px)'
        menu.style.height = '0px'
        condition = false
    }
    else{
        menu.style.height = '320px'
        menu.style.transform='translateY(0px)'
        condition = true
        
        }
})