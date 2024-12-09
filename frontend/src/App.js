import React, { useState } from 'react';
import axios from 'axios';

function App() {
    const [targetStations, setTargetStations] = useState(50);
    const [eps, setEps] = useState(0.05);
    const [minSamples, setMinSamples] = useState(8);
    const [results, setResults] = useState([]);
    const [errorMessage, setErrorMessage] = useState('');

    const handleOptimize = () => {
        axios.post(
            `${process.env.REACT_APP_API_URL}/optimize-bus-stations`,
            {
                target_stations: targetStations,
                eps: eps,
                min_samples: minSamples,
            },
            { headers: { "Content-Type": "application/json" } }
        )
        .then(response => {
            const newResult = {
                dbscanCsvLink: `${process.env.REACT_APP_API_URL}/files/${response.data.dbscan_csv_path}`,
                kmeansCsvLink: `${process.env.REACT_APP_API_URL}/files/${response.data.kmeans_csv_path}`,
                comparisonImage: `${process.env.REACT_APP_API_URL}/files/${response.data.comparison_image}`,
            };
            setResults([newResult, ...results]); // 新结果放在数组首位
            setErrorMessage('');
        })
        .catch(error => {
            console.error("Error:", error.response?.data || error.message);
            setErrorMessage('Error: Unable to optimize bus stations. Please try again.');
        });
    };

    return (
        <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif', color: 'black', backgroundColor: '#f8f5f2' }}>
            <h1 style={{ textAlign: 'center', color: 'orange' }}>Bus Station Optimization</h1>
            <p style={{ textAlign: 'center', fontSize: '14px', color: '#333' }}>
                Optimize bus station locations using DBSCAN and KMeans clustering algorithms.
            </p>

            <div style={{ margin: '20px auto', maxWidth: '600px', backgroundColor: '#fff', padding: '20px', borderRadius: '8px', boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)' }}>
                <label style={{ display: 'block', marginBottom: '15px', fontWeight: 'bold' }}>
                    Target Stations: <span style={{ color: 'orange' }}>{targetStations}</span>
                    <input
                        type="range"
                        min="10"
                        max="200"
                        step="10"
                        value={targetStations}
                        onChange={(e) => setTargetStations(Number(e.target.value))}
                        style={{ width: '100%', marginTop: '10px' }}
                    />
                </label>

                <label style={{ display: 'block', marginBottom: '15px', fontWeight: 'bold' }}>
                    Eps (DBSCAN Radius): <span style={{ color: 'orange' }}>{eps.toFixed(2)}</span>
                    <input
                        type="range"
                        min="0.01"
                        max="1"
                        step="0.01"
                        value={eps}
                        onChange={(e) => setEps(Number(e.target.value))}
                        style={{ width: '100%', marginTop: '10px' }}
                    />
                </label>

                <label style={{ display: 'block', marginBottom: '15px', fontWeight: 'bold' }}>
                    Min Samples: <span style={{ color: 'orange' }}>{minSamples}</span>
                    <input
                        type="range"
                        min="1"
                        max="50"
                        step="1"
                        value={minSamples}
                        onChange={(e) => setMinSamples(Number(e.target.value))}
                        style={{ width: '100%', marginTop: '10px' }}
                    />
                </label>

                <button
                    onClick={handleOptimize}
                    style={{
                        width: '100%',
                        padding: '10px',
                        fontSize: '16px',
                        fontWeight: 'bold',
                        color: '#fff',
                        backgroundColor: 'orange',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: 'pointer',
                        marginTop: '10px',
                    }}
                >
                    Optimize
                </button>

                {errorMessage && <p style={{ color: 'red', marginTop: '15px', fontWeight: 'bold' }}>{errorMessage}</p>}
            </div>

            {results.map((result, index) => (
                <div key={index} style={{ marginTop: '20px', textAlign: 'center' }}>
                    <h3 style={{ color: 'orange' }}>Optimization Result {index + 1}</h3>
                    <a
                        href={result.dbscanCsvLink}
                        download
                        style={{ display: 'inline-block', margin: '10px 0', textDecoration: 'none', color: 'orange', fontWeight: 'bold' }}
                    >
                        Download DBSCAN CSV
                    </a>
                    <br />
                    <a
                        href={result.kmeansCsvLink}
                        download
                        style={{ display: 'inline-block', margin: '10px 0', textDecoration: 'none', color: 'orange', fontWeight: 'bold' }}
                    >
                        Download KMeans CSV
                    </a>
                    <br />
                    <img
                        src={result.comparisonImage}
                        alt={`Comparison Result ${index + 1}`}
                        style={{ maxWidth: '100%', borderRadius: '8px', marginTop: '20px', border: '2px solid orange' }}
                    />
                </div>
            ))}
        </div>
    );
}

export default App;