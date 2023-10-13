let blocks=document.getElementsByClassName('block')
let pages=document.getElementsByClassName('page')
let triangls=document.getElementsByClassName('triangle')
for(let i=0;i<blocks.length;i++)
{
    blocks[i].onclick=function(){
        for(let j=0;j<pages.length;j++)
        {
            if(blocks[j]==this){
                blocks[j].classList.add('current')
                pages[j].classList.add('current')
                triangls[j].classList.add('current')
            }
            else{
                blocks[j].classList.remove('current')
                pages[j].classList.remove('current')
                triangls[j].classList.remove('current')
            }
        }
    }
}