// "use strict";

// console.log('react is loading');

// // need to figure out how to load this: basically, when I click on a marker, I want to add
// // comments / rating to the farm
// const Add = (props) => {
//     // const [FarmComment, setFarmComment] = React.useState([]);
//     const [url, setURL] = React.useState('')

//     makeMarker(centerLon, centerLat, lon, lat, link, zoom) 

//     // React.useEffect(() => {
//     //     // need to write to sqlalchemy (not sure how to do it)
//     //     let comment = document.querySelector('.formContent').value
//     //     // set it to when content is changed?
//     //   }, [])
    
//     // how do I refer to a google marker here?
//     function newFarm() {
//         const url = props.link;
//         setURL(url);
//     }
  
//     return (

//         <React.Fragment>
//             <form action='/api/comments' onSubmit={e => e.preventDefault()}>
//                 <h3 className="formTitle"> Add a bookmark</h3>
//                 <div>
//                     <label
//                         htmlFor="linkTitle"
//                         // need to be able to do request.form.get on url (need to do comments.js to do this?)
//                         className="formLabel">Add {url} to bookmark?</label>
//                 </div> 
//                 {/* <div>
//                     <label
//                     htmlFor="comments"
//                     className="formComment"> Enter your comments</label>
//                     <input
//                         // need to be able to do request.form.get to get comment
//                         value={newFarmComment}
//                         className='formContent'
//                         // I don't actually think that I want to use this as a function that calls for rendering...
//                         onChange={e =>setFarmComment(e.currentTarget.value)}
//                         type="text"
//                         name="comments" />
//                 </div> */}
//                 {/* I want to be able to submit this data to backend once the button Add is clicked. */}
//                 <button>Add</button>
//             </form>

//         </React.Fragment>
//         )
//     }

// ReactDOM.render(
//     <Add link={window.value} />,
//     document.getElementById('root')
// )

// // function Add(){
    
// // }