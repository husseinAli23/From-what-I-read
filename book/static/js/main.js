// get all stars
const one = document.querySelector('#first')
const two = document.getElementById('second')
const three = document.getElementById('third')
const four = document.getElementById('fourth')
const five = document.getElementById('fifth')

const form = document.querySelector('.rate-form')
// no need done:
// const confirmBox = document.getElementById('confirm-box')
const csrf = document.getElementsByName('csrfmiddlewaretoken')

const handleStarSelect = (size) => {
    const children = form.children
    for (let i = 0; i < children.length; i++) {
        if (i <= size) {
            children[i].classList.add('checked')
        } else {
            children[i].classList.remove('checked')
        }
    }
}

// longer version - to be optimized
const handleSelect = (selection) => {
    switch (selection) {
        case 'first': {
            // one.classList.add('checked')
            // two.classList.remove('checked')
            // three.classList.remove('checked')
            // four.classList.remove('checked')
            // five.classList.remove('checked')
            handleStarSelect(1)
            return
        }
        case 'second': {
            handleStarSelect(2)
            return
        }
        case 'third': {
            handleStarSelect(3)
            return
        }
        case 'fourth': {
            handleStarSelect(4)
            return
        }
        case 'fifth': {
            handleStarSelect(5)
            return
        }
        default: {
            handleStarSelect(0)
        }
    }
}

const arr = [one, two, three, four, five]
if(one){
    arr.forEach(item=> item.addEventListener('mouseover', (event)=>{
    
        handleSelect(event.target.id)
    }))
    
    arr.forEach(item=> item.addEventListener('click', (event)=>{
    
         handleSelect(event.target.id)
        }))
 }


const getNumericValue = (stringValue) => {
    let numericValue;
    if (stringValue === 'first') {
        numericValue = 1
    }
    else if (stringValue === 'second') {
        numericValue = 2
    }
    else if (stringValue === 'third') {
        numericValue = 3
    }
    else if (stringValue === 'fourth') {
        numericValue = 4
    }
    else if (stringValue === 'fifth') {
        numericValue = 5
    }
    else {
        numericValue = 0
    }
    return numericValue
}
console.log(one)
if (one) {
    const arr = [one, two, three, four, five]

     arr.forEach(item => item.addEventListener('mouseover', (event) => {
        
         handleSelect(event.target.id)
     }))

    arr.forEach(item => item.addEventListener('mouseover', (event) => {
        

        // value of the rating not numeric
        const val = event.target.id

        /* handleSelect(event.target.id) */
            isSubmit = true
            // picture id
            const id = event.target.id
            // value of the rating translated into numeric
            const val_num = getNumericValue(val)
      
            $('#rate_input').val(getNumericValue(event.target.id))
      
            // axios.post("/rating/", {
            //     'csrfmiddlewaretoken': csrf[0].value,
            //     'el_id': id,
            //     'val': val_num,
            // }).then(function (response) {
            //     console.log(response)
            //     confirmBox.innerHTML = `<h1>Successfully rated with ${response.score}</h1>`
            // }).catch(function (error) {
            //     console.log(error)
            //     confirmBox.innerHTML = '<h1>Ups... something went wrong</h1>'
            // })
      
    }))
}


