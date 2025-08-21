import React, { useState, useEffect } from 'react'

const API = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export default function App(){
  const [token, setToken] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [user, setUser] = useState(null)
  const [title, setTitle] = useState('Demo TaoWorks AI')
  const [topic, setTopic] = useState('AI in Education')
  const [rawText, setRawText] = useState('')
  const [items, setItems] = useState([])

  const login = async () => {
    const form = new URLSearchParams()
    form.append('username', email)
    form.append('password', password)
    const r = await fetch(`${API}/auth/login`, { method:'POST', body: form })
    const j = await r.json()
    if(j.access_token){
      setToken(j.access_token)
      setUser(j.user)
      loadList(j.user.id)
    } else {
      alert('Login failed')
    }
  }

  const register = async () => {
    const r = await fetch(`${API}/auth/register?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`, { method:'POST' })
    if(r.ok){ alert('Đăng ký thành công. Hãy đăng nhập!') }
    else { alert('Đăng ký thất bại') }
  }

  const loadList = async (uid) => {
    const r = await fetch(`${API}/presentations?user_id=${uid}`)
    const j = await r.json()
    setItems(j)
  }

  const gen = async () => {
    if(!user){ alert('Hãy đăng nhập trước'); return }
    const form = new FormData()
    form.append('user_id', user.id)
    form.append('title', title)
    form.append('topic', topic)
    form.append('raw_text', rawText)
    const r = await fetch(`${API}/generate`, { method:'POST', body: form })
    const j = await r.json()
    loadList(user.id)
    alert('Đã tạo!')
  }

  return (
    <div style={{fontFamily:'system-ui, sans-serif', padding:20, maxWidth:900, margin:'0 auto'}}>
      <h1>TaoWorks AI</h1>

      {!user && (
        <div style={{display:'grid', gap:8, maxWidth:360}}>
          <input placeholder='Email' value={email} onChange={e=>setEmail(e.target.value)} />
          <input placeholder='Mật khẩu' type='password' value={password} onChange={e=>setPassword(e.target.value)} />
          <div style={{display:'flex', gap:8}}>
            <button onClick={login}>Đăng nhập</button>
            <button onClick={register}>Đăng ký</button>
          </div>
        </div>
      )}

      {user && (
        <>
          <p>Xin chào, <b>{user.name || user.email}</b></p>
          <div style={{border:'1px solid #ddd', padding:12, borderRadius:8, marginTop:12}}>
            <h3>Tạo bài thuyết trình</h3>
            <input value={title} onChange={e=>setTitle(e.target.value)} placeholder='Tiêu đề' />
            <input value={topic} onChange={e=>setTopic(e.target.value)} placeholder='Chủ đề' />
            <textarea rows={6} value={rawText} onChange={e=>setRawText(e.target.value)} placeholder='(Tùy chọn) Văn bản đầu vào'/>
            <div><button onClick={gen}>Tạo</button></div>
          </div>

          <h3 style={{marginTop:24}}>Lịch sử</h3>
          <ul>
            {items.map(it => (
              <li key={it.id} style={{marginBottom:6}}>
                <b>{it.title}</b> — 
                {it.pptx_path && <a href={`${API.replace('8000','8000')}/${it.pptx_path}`} download style={{marginLeft:8}}>Tải PPTX</a>}
                {it.pdf_path && <a href={`${API.replace('8000','8000')}/${it.pdf_path}`} download style={{marginLeft:8}}>PDF</a>}
                {it.audio_path && <a href={`${API.replace('8000','8000')}/${it.audio_path}`} download style={{marginLeft:8}}>Audio</a>}
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  )
}
