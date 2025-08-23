import { useEffect } from 'react'
import './App.scss'

import Home from './pages/home/home.tsx'

function App() {
  const useReactQuerySubscription = () => {
    useEffect(() => {
      const protocol = window.location.protocol === "https:" ? "wss" : "ws";
      const wsUrl = `${protocol}://${window.location.host}/api/ws`;

      const websocket = new WebSocket(wsUrl);
      websocket.onopen = () => {
        console.log('Websocket connected')
      }

      return () => {
        websocket.close()
      }
    }, [])
  }
  useReactQuerySubscription();

  return (
    <Home />
  )
}

export default App
