import { useEffect, useMemo, useRef, useState } from 'react'
import { Chess } from 'chess.js'
import stockfishWorkerUrl from 'stockfish/bin/stockfish-18-lite-single.js?url'
import stockfishWasmUrl from 'stockfish/bin/stockfish-18-lite-single.wasm?url'
import './App.css'

const files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
const pieces = {
  wp: '♙',
  wn: '♘',
  wb: '♗',
  wr: '♖',
  wq: '♕',
  wk: '♔',
  bp: '♟',
  bn: '♞',
  bb: '♝',
  br: '♜',
  bq: '♛',
  bk: '♚',
}

function makeGame() {
  return new Chess()
}

function cloneGame(game) {
  const nextGame = new Chess()

  game.history({ verbose: true }).forEach((move) => {
    nextGame.move({
      from: move.from,
      to: move.to,
      promotion: move.promotion,
    })
  })

  return nextGame
}

function makeSquares() {
  return Array.from({ length: 8 }, (_, rankIndex) =>
    Array.from({ length: 8 }, (_, fileIndex) => {
      const rank = 8 - rankIndex
      return `${files[fileIndex]}${rank}`
    }),
  ).flat()
}

function statusFor(game, engineReady, aiThinking, engineError) {
  if (engineError) return engineError

  if (game.isCheckmate()) {
    return game.turn() === 'w' ? 'Checkmate. Stockfish wins.' : 'Checkmate. You win.'
  }

  if (game.isDraw()) {
    if (game.isStalemate()) return 'Draw by stalemate.'
    if (game.isThreefoldRepetition()) return 'Draw by repetition.'
    if (game.isInsufficientMaterial()) return 'Draw by insufficient material.'
    return 'Draw.'
  }

  if (aiThinking) return 'Stockfish is thinking.'
  if (!engineReady) return 'Loading Stockfish.'
  if (game.inCheck()) return game.turn() === 'w' ? 'Your king is in check.' : 'Stockfish is in check.'

  return game.turn() === 'w' ? 'Your move.' : 'Stockfish to move.'
}

function App() {
  const [game, setGame] = useState(makeGame)
  const [selected, setSelected] = useState(null)
  const [engineReady, setEngineReady] = useState(false)
  const [engineError, setEngineError] = useState('')
  const [aiThinking, setAiThinking] = useState(false)
  const [skill, setSkill] = useState(8)
  const [lastMove, setLastMove] = useState(null)
  const workerRef = useRef(null)
  const pendingBestMoveRef = useRef(false)

  const squares = useMemo(() => makeSquares(), [])
  const legalTargets = useMemo(() => {
    if (!selected || game.turn() !== 'w' || game.isGameOver()) return new Set()
    return new Set(game.moves({ square: selected, verbose: true }).map((move) => move.to))
  }, [game, selected])

  const board = game.board()
  const status = statusFor(game, engineReady, aiThinking, engineError)

  useEffect(() => {
    const engineUrl = `${stockfishWorkerUrl}#${encodeURIComponent(stockfishWasmUrl)}`
    const worker = new Worker(engineUrl)
    workerRef.current = worker

    function handleEngineLine(line) {
      const trimmedLine = line.trim()

      if (trimmedLine === 'uciok') {
        worker.postMessage('isready')
        return
      }

      if (trimmedLine === 'readyok') {
        setEngineReady(true)
        return
      }

      if (!trimmedLine.startsWith('bestmove') || !pendingBestMoveRef.current) return

      pendingBestMoveRef.current = false
      setAiThinking(false)
      const [, bestMove] = trimmedLine.split(' ')

      if (!bestMove || bestMove === '(none)') return

      setGame((currentGame) => {
        const nextGame = cloneGame(currentGame)
        const move = nextGame.move({
          from: bestMove.slice(0, 2),
          to: bestMove.slice(2, 4),
          promotion: bestMove.slice(4, 5) || 'q',
        })

        if (!move) return currentGame
        setLastMove({ from: move.from, to: move.to })
        return nextGame
      })
    }

    worker.onmessage = (event) => {
      String(event.data).split('\n').forEach(handleEngineLine)
    }

    worker.onerror = () => {
      setEngineError('Stockfish failed to load.')
      setAiThinking(false)
      pendingBestMoveRef.current = false
    }

    worker.postMessage('uci')

    return () => {
      worker.postMessage('quit')
      worker.terminate()
      workerRef.current = null
    }
  }, [])

  useEffect(() => {
    if (!engineReady || !workerRef.current) return
    workerRef.current.postMessage(`setoption name Skill Level value ${skill}`)
  }, [engineReady, skill])

  useEffect(() => {
    if (!engineReady || game.turn() !== 'b' || game.isGameOver() || pendingBestMoveRef.current) {
      return
    }

    pendingBestMoveRef.current = true
    setAiThinking(true)
    workerRef.current.postMessage('ucinewgame')
    workerRef.current.postMessage(`position fen ${game.fen()}`)
    workerRef.current.postMessage(`go depth ${Math.max(4, skill + 2)}`)
  }, [engineReady, game, skill])

  function resetGame() {
    pendingBestMoveRef.current = false
    setAiThinking(false)
    setSelected(null)
    setLastMove(null)
    setGame(makeGame())
    workerRef.current?.postMessage('stop')
    workerRef.current?.postMessage('ucinewgame')
  }

  function selectSquare(square) {
    if (game.turn() !== 'w' || game.isGameOver() || aiThinking) return

    const piece = game.get(square)

    if (!selected) {
      if (piece?.color === 'w') setSelected(square)
      return
    }

    if (selected === square) {
      setSelected(null)
      return
    }

    if (piece?.color === 'w') {
      setSelected(square)
      return
    }

    const nextGame = cloneGame(game)
    const move = nextGame.move({ from: selected, to: square, promotion: 'q' })

    if (!move) return

    setSelected(null)
    setLastMove({ from: move.from, to: move.to })
    setGame(nextGame)
  }

  return (
    <main className="app-shell">
      <section className="game-panel" aria-label="Local chess game">
        <div className="board-wrap">
          <div className="rank-labels" aria-hidden="true">
            {[8, 7, 6, 5, 4, 3, 2, 1].map((rank) => (
              <span key={rank}>{rank}</span>
            ))}
          </div>

          <div className="board" role="grid" aria-label="Chess board">
            {squares.map((square) => {
              const fileIndex = files.indexOf(square[0])
              const rankIndex = 8 - Number(square[1])
              const piece = board[rankIndex][fileIndex]
              const isDark = (fileIndex + rankIndex) % 2 === 1
              const isSelected = selected === square
              const isLegalTarget = legalTargets.has(square)
              const isLastMove = lastMove?.from === square || lastMove?.to === square

              return (
                <button
                  className={[
                    'square',
                    isDark ? 'dark' : 'light',
                    isSelected ? 'selected' : '',
                    isLegalTarget ? 'legal' : '',
                    isLastMove ? 'last-move' : '',
                  ]
                    .filter(Boolean)
                    .join(' ')}
                  key={square}
                  type="button"
                  role="gridcell"
                  aria-label={`${square}${piece ? ` ${piece.color === 'w' ? 'white' : 'black'} ${piece.type}` : ''}`}
                  onClick={() => selectSquare(square)}
                >
                  <span className={`piece ${piece?.color ?? ''}`}>
                    {piece ? pieces[`${piece.color}${piece.type}`] : ''}
                  </span>
                </button>
              )
            })}
          </div>

          <div className="file-labels" aria-hidden="true">
            {files.map((file) => (
              <span key={file}>{file}</span>
            ))}
          </div>
        </div>
      </section>

      <aside className="side-panel" aria-label="Game controls">
        <div>
          <p className="eyebrow">Local React Chess</p>
          <h1>Play Stockfish</h1>
          <p className="status">{status}</p>
        </div>

        <div className="controls">
          <label htmlFor="skill">
            <span>AI skill</span>
            <strong>{skill}</strong>
          </label>
          <input
            id="skill"
            max="20"
            min="0"
            type="range"
            value={skill}
            onChange={(event) => setSkill(Number(event.target.value))}
          />
        </div>

        <button className="primary-action" type="button" onClick={resetGame}>
          New game
        </button>

        <div className="move-list">
          <h2>Moves</h2>
          <ol>
            {game.history().map((move, index) => (
              <li key={`${move}-${index}`}>{move}</li>
            ))}
          </ol>
        </div>
      </aside>
    </main>
  )
}

export default App
