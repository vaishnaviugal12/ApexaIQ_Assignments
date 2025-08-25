// src/App.jsx
import { useEffect, useState } from "react";

const NASA_KEY = import.meta.env.VITE_NASA_KEY;
const API_URL = `https://api.nasa.gov/planetary/apod?api_key=${NASA_KEY}&count=60`;

function App() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // pagination
  const [page, setPage] = useState(1);
  const itemsPerPage = 9;

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);
        const res = await fetch(API_URL);
        if (!res.ok) throw new Error("Failed to fetch data");
        const json = await res.json();
        setData(json);
        setError(null);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  const totalPages = Math.ceil(data.length / itemsPerPage);
  const start = (page - 1) * itemsPerPage;
  const pageData = data.slice(start, start + itemsPerPage);

  if (loading) return <p className="text-center mt-10">Loading...</p>;
  if (error) return <p className="text-center mt-10 text-red-500">{error}</p>;

  return (
    <div className="p-6 space-y-6 max-w-7xl mx-auto">
      <header className="flex items-end justify-between gap-4 flex-wrap">
        <div>
          <h2 className="text-2xl font-semibold">Astronomy Picture of the Day</h2>
          <p className="text-gray-400 text-sm">Last 60 days • {data.length} items</p>
        </div>
        <Pagination page={page} setPage={setPage} totalPages={totalPages} />
      </header>

      {/* Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {pageData.map((it) => (
          <ApodCard key={it.date} item={it} />
        ))}
      </div>

      <Pagination page={page} setPage={setPage} totalPages={totalPages} />
    </div>
  );
}

// Card Component
function ApodCard({ item }) {
  const isVideo = item.media_type === "video";
  return (
    <article className="bg-gray-900 border border-gray-800 rounded-2xl overflow-hidden shadow">
      <div className="aspect-video bg-gray-800">
        {isVideo ? (
          <iframe
            className="w-full h-full"
            src={item.url}
            title={item.title}
            allowFullScreen
          />
        ) : (
          <img
            src={item.url}
            alt={item.title}
            className="w-full h-full object-cover"
          />
        )}
      </div>
      <div className="p-4 space-y-2">
        <h3 className="font-semibold text-gray-300 leading-tight">{item.title}</h3>
        <p className="text-xs text-gray-400">{item.date}</p>
        <p className="text-sm text-gray-300 line-clamp-3">{item.explanation}</p>
        {item.hdurl && !isVideo && (
          <a
            className="inline-block mt-2 text-sm underline hover:no-underline"
            href={item.hdurl}
            target="_blank"
            rel="noreferrer"
          >
            Open HD
          </a>
        )}
      </div>
    </article>
  );
}

// Pagination Component
function Pagination({ page, setPage, totalPages }) {
  return (
    <div className="flex items-center gap-2">
      <button
        onClick={() => setPage((p) => Math.max(1, p - 1))}
        disabled={page === 1}
        className="px-3 py-1 bg-blue-500 rounded disabled:opacity-50"
      >
        Prev
      </button>
      <span className="text-sm">
        Page {page} of {totalPages}
      </span>
      <button
        onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
        disabled={page === totalPages}
        className="px-3 py-1 bg-blue-500 rounded disabled:opacity-50"
      >
        Next
      </button>
    </div>
  );
}

export default App;
