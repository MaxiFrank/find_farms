"use strict";

console.log('react is loading');

// need to figure out how to load this: basically, when I click on a marker, I want to add
// comments / rating to the farm
const Add = (props) => {
    const [newFarmComment, setNewFarmComment] = React.useState([]);

    React.useEffect(() => {
        // need to write to sqlalchemy (not sure how to do it)
        let comment = document.querySelector('.formContent').value
        // set it to when content is changed?
      }, [])
    
  
    return (

        <React.Fragment>
            <form onSubmit={e => e.preventDefault()}>
                <h3 className="formTitle"> Add a bookmark</h3>
                <div>
                    <label
                        htmlFor="linkTitle"
                        className="formLabel">Add {props.link} to bookmark?</label>
                </div> 
                <div>
                    <label
                    htmlFor="comments"
                    className="formComment"> Enter your comments</label>
                    <input
                        value={newFarmComment}
                        className='formContent'
                        onChange={e =>setNewFarmComment(e.currentTarget.value)}
                        type="text"
                        name="comments" />
                </div>
                <button>Add</button>
            </form>

        </React.Fragment>
        )
    }

ReactDOM.render(
    <Add link='https://www.workaway.info/en/host/555487858567' />,
    document.getElementById('root')
)