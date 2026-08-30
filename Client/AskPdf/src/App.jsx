import { useState } from 'react'
import heroImg from './assets/hero.png'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import './App.css'

function App() {
  const [text, settext] = useState("")

  const [loader, setloader] = useState(false)
const [files, setfiles] = useState([])
const [message, setmessage] = useState("")
const [response, setresponse] = useState("")
  const handleadd =  async ()=>{

    try {
      setloader(true)
      if(files.length === 0){
        return setmessage("Please upload a PDF , file or a document before asking a question.")
      }

      const formdata = new FormData()
      files.forEach(file=>{
        formdata.append("filesparameter" , file)
      })
      
      if(text){
        formdata.append("text" , text)
      }
     


      
    const request = await fetch(`http://127.0.0.1:8000/search` , {
      method: "POST",
      body: formdata
      
    })

    const response = await request.json()
    if(request.ok){
      setresponse(response)
    }

    else{
      setmessage(response.message)
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
     <div className="app">

      {/* Sidebar */}
      <aside className="sidebar">

        <div className="brand">
          <div className="brand-icon">✦</div>
          <h2>AskMyPDF</h2>
        </div>

        <button className="new-chat-btn">
          + New Chat
        </button>

        <div className="sidebar-section">
          <p className="section-title">Your Documents</p>

          <div className="document-item active">
            <span className="pdf-icon">PDF</span>
            <div className="document-info">
              <span className="document-name">
                My Resume.pdf
              </span>
              <span className="document-meta">
                8 pages
              </span>
            </div>
          </div>
          <div className="document-item">
            <span className="pdf-icon">PDF</span>
            <div className="document-info">
              <span className="document-name">
                Health Records.pdf
              </span>
              <span className="document-meta">
                13 pages
              </span>
            </div>
          </div>
        </div>

        <button className="upload-btn">
          <span>↑</span>
          Upload PDF
        </button>

        

      </aside>


      {/* Main Area */}
      <main className="main">

        {/* Header */}
        <header className="topbar">

          <div>
            <h1>Ask your documents</h1>
            <p>Get answers from your PDFs using AI.</p>
          </div>

        

        </header>


        {/* Chat Area */}
        <section className="chat-area">

          {/* Empty State */}
          <div className="empty-state">

            <div className="empty-icon">
              ✦
            </div>

            <h2>What would you like to know?</h2>

            <p>
              Ask a question about your documents and
              get an answer based on their contents.
            </p>

            <div className="suggestions">

             

              <button>
                Summarize this document
              </button>

              <button>
                What are the main points?
              </button>

            </div>

          </div>


          {/* Messages will come here later */}
          <div className="messages">
            {response.answer}
          </div>

        </section>


        {/* Input Area */}
        <div className="input-wrapper">

          <div className="question-box">
            <textarea value={text} onChange={(e)=>{settext(e.target.value) ; setmessage("")}} placeholder='Ask anything about your documents...'
            >
            </textarea>
            <p id='error'> {message}</p>


            {response.message &&(
<>
<p id='message'> {response.message}</p>
</>
            )}
           


            <label className="file-upload">
  <span className="upload-icon">📎</span>
  <span>Attach PDF</span>

  <input
    type="file"
    multiple
    accept=".pdf"
    onChange={handlefile}
  />
</label>



            <div className="input-bottom">

              <div className="selected-document">
                <span className="small-pdf-icon">PDF</span>
                My Resume.pdf
              </div>

              <button onClick={handleadd} className="send-btn">
                {loader ? (
                  <>
                  <div className="loader"></div>
                  </>


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
