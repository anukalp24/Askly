import { useState } from 'react'
import toast, { Toaster } from 'react-hot-toast'

// once in your App, anywhere in the JSX tree:
import './App.css'
function App() {
  const [question, setquestion] = useState("")
  const [response, setresponse] = useState([])

  const [loader, setloader] = useState(false)
const [files, setfiles] = useState([])
const [message, setmessage] = useState(null)
  const handleadd =  async ()=>{
    

    try {
      setloader(true)
      if(files.length === 0 && !localStorage.getItem("session_id")){
       
       return toast.error("Upload pdf to get started")
      }

      

      const formdata = new FormData()
      files.forEach(file=>{
        formdata.append("filesparameter" , file)
      })
      
      if(question){
        formdata.append("question" , question)
      }
     


      if(files.length === 0 && localStorage.getItem("session_id")){
        
          const req = await fetch(`http://127.0.0.1:8000/ask` , {
            method: "POST" ,
            body:formdata ,
            credentials: "include"
          })
          const result = await req.json()

          if(req.ok){
            setquestion("")

            setresponse([... response , result])
            setfiles([])
          }

          else{
            // setmessage(result.message)
            toast.error(result.message)
          }
        
      }
      else{
        
          const req = await fetch(`http://127.0.0.1:8000/upload` , {
            method: "POST" ,
            body:formdata , 
            credentials:"include"
          })
          const result = await req.json()


          if(req.ok){
            setquestion("")
            setresponse([... response , result])
            localStorage.setItem("session_id" , result.session_id)
          }

          else{
            // setmessage(result.message)
               toast.error(result.message)
          }
       
      }
     
    } catch (error) {
      setmessage(error.message)
    }

    finally{
      setloader(false)
    }
   
  }
  

  const handlefile = (e)=>{
    setmessage("")
    setfiles([...files , ...e.target.files])
  }   
  return (
    <>
 <Toaster
        position="top-center"
        toastOptions={{ duration: 3000 }}
      />

      <div className="app">

        {/* Desktop Sidebar */}
        <aside className="sidebar">

          <div className="brand">
            <div className="brand-icon">✦</div>
            <h2>AskMyPDF</h2>
          </div>

          <button
            disabled={!localStorage.getItem("session_id")}
            className="new-chat-btn"
            onClick={() => {
              localStorage.removeItem("session_id")
              setresponse([])
              setfiles([])
              toast.success("Started a new session")
            }}
          >
            + New Chat
          </button>

        </aside>


        {/* Main Area */}
        <main className="main">

          {/* Mobile Navbar */}
          <div className="mobile-navbar">

            <div className="mobile-brand">
              <div className="brand-icon">✦</div>
              <h2>AskMyPDF</h2>
            </div>

            <button
              disabled={!localStorage.getItem("session_id")}
              className="mobile-new-chat"
              onClick={() => {
                localStorage.removeItem("session_id")
                setresponse([])
                setfiles([])
                 setquestion("")
                toast.success("Started a new session")
              }}
            >
              + New Chat
            </button>

          </div>


          {/* Header */}
          <header className="topbar">

            <div>
              <h1>Chat with your PDFs</h1>
              <p>
                Ask questions and get answers from your documents.
              </p>
            </div>

          </header>


          {/* Chat Area */}
          <section className="chat-area">

            {/* Empty State */}
            {response.length === 0 && (
              <div className="empty-state">

                <div className="empty-icon">
                  ✦
                </div>

                <h2>What would you like to know?</h2>

                <p>
                  Ask a question about your documents and
                  get an answer based on their contents.
                </p>

            

              </div>
            )}


            {/* Messages */}
            <div className="messages">

              {response.map((val, index) => (

                <div
                  className="message-pair"
                  key={index}
                >

                  <div className="message user-message">

                    <div className="message-role">
                      You
                    </div>

                    <p>
                      {val.question}
                    </p>

                  </div>


                  <div className="message ai-message">

                    <div className="message-role">
                      Ask-My-PDF
                    </div>

                    <p>
                      {val.answer}
                    </p>

                  </div>

                </div>

              ))}

            </div>

          </section>


          {/* Input Area */}
          <div className="input-wrapper">

            <div className="question-box">

              <textarea
                value={question}
                onChange={(e) => {
                  setquestion(e.target.value)
                  setmessage("")
                }}
                placeholder="Ask anything about your documents..."
              />

              <p id="error"></p>


              {message && (
                <p id="message">
                  {message}
                </p>
              )}


              {/* File Upload */}
              <label className="file-upload">

                <span className="upload-icon">
                  📎
                </span>

                <span>
                  Attach PDF
                </span>

                <input
                  type="file"
                  multiple
                  accept=".pdf"
                  onChange={handlefile}
                />

              </label>


              {/* Input Bottom */}
              <div className="input-bottom">

                <div className="selected-document">

                  <span className="small-pdf-icon">
                    PDF
                  </span>


                  {files.length > 0 ? (

                    <>
                      {files.map((pdf, index) => (

                        <div key={index}>
                          <p>{pdf.name}</p>
                        </div>

                      ))}
                    </>

                  ) : (

                    <span className="file-name">
                      No file selected
                    </span>

                  )}

                </div>


                {/* Send Button */}
                <button
                  onClick={handleadd}
                  className="send-btn"
                >

                  {loader ? (

                    <div className="loader"></div>

                  ) : (

                    <>
                      ↑
                    </>

                  )}

                </button>

              </div>

            </div>


            <p className="input-note">
              Answers are generated from your uploaded documents.
            </p>

          </div>

        </main>

      </div>
  

</>
  )
}

export default App
