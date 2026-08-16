import { useEffect, useState } from 'react'

const API = '/api/tasks'

function App() {
  const [tasks, setTasks] = useState([])
  const [description, setDescription] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const loadTasks = async () => {
    try {
      const response = await fetch(API)
      if (!response.ok) throw new Error('Unable to load tasks')
      const data = await response.json()
      setTasks(data)
      setError('')
    } catch (err) {
      setError('Unable to load tasks right now.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadTasks()
  }, [])

  const addTask = async (event) => {
    event.preventDefault()
    const trimmed = description.trim()

    if (!trimmed) return

    try {
      const response = await fetch(API, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ description: trimmed }),
      })

      if (!response.ok) {
        const data = await response.json()
        throw new Error(data.error || 'Unable to add task')
      }

      const newTask = await response.json()
      setTasks((current) => [newTask, ...current])
      setDescription('')
      setError('')
    } catch (err) {
      setError(err.message)
    }
  }

  const toggleTask = async (taskId) => {
    try {
      const response = await fetch(`${API}/${taskId}`, {
        method: 'PATCH',
      })

      if (!response.ok) throw new Error('Unable to update task')

      const updatedTask = await response.json()
      setTasks((current) =>
        current.map((task) => (task.id === updatedTask.id ? updatedTask : task)),
      )
    } catch (err) {
      setError(err.message)
    }
  }

  const deleteTask = async (taskId) => {
    try {
      const response = await fetch(`${API}/${taskId}`, {
        method: 'DELETE',
      })

      if (!response.ok) throw new Error('Unable to delete task')

      setTasks((current) => current.filter((task) => task.id !== taskId))
    } catch (err) {
      setError(err.message)
    }
  }

  const completedCount = tasks.filter((task) => task.completed).length
  const pendingCount = tasks.length - completedCount
  const percent = tasks.length ? Math.round((completedCount / tasks.length) * 100) : 0

  return (
    <div className="app-shell">
      <div className="container">
        <header className="app-header">
          <p className="eyebrow">Task management</p>
          <h1>Task Tracker</h1>
        </header>

        <section className="stats-bar" aria-label="Task statistics">
          <div className="stat-item">
            <span className="stat-value">{tasks.length}</span>
            <span className="stat-label">Total</span>
          </div>
          <div className="stat-item">
            <span className="stat-value completed-count">{completedCount}</span>
            <span className="stat-label">Completed</span>
          </div>
          <div className="stat-item">
            <span className="stat-value pending-count">{pendingCount}</span>
            <span className="stat-label">Pending</span>
          </div>
          <div className="stat-item">
            <span className="stat-value">{percent}%</span>
            <span className="stat-label">Progress</span>
          </div>
        </section>

        <form className="task-form" onSubmit={addTask}>
          <input
            type="text"
            value={description}
            onChange={(event) => setDescription(event.target.value)}
            placeholder="Add a new task..."
            maxLength={255}
            aria-label="Task description"
          />
          <button type="submit">Add</button>
        </form>

        {error && <p className="error-message">{error}</p>}

        {loading ? (
          <p className="empty-state">Loading tasks...</p>
        ) : tasks.length === 0 ? (
          <div className="empty-state">
            <h2>No tasks yet</h2>
            <p>Add your first task above.</p>
          </div>
        ) : (
          <ul className="task-list">
            {tasks.map((task) => (
              <li key={task.id} className={task.completed ? 'task-item completed' : 'task-item'}>
                <div className="task-main">
                  <button
                    type="button"
                    className={task.completed ? 'checkbox completed' : 'checkbox'}
                    onClick={() => toggleTask(task.id)}
                    aria-label={task.completed ? 'Mark task as incomplete' : 'Mark task as complete'}
                  >
                    {task.completed ? '✓' : ''}
                  </button>
                  <span className="task-text">{task.description}</span>
                </div>

                <button type="button" className="delete-button" onClick={() => deleteTask(task.id)}>
                  Remove
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}

export default App
