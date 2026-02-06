import React from 'react';

const ResultCard = ({ result }) => {
    if (!result) return null;

    const { verdict, safety_score, risk_breakdown, signals, layers } = result;

    // Color coding based on verdict
    let statusColor = "var(--text-muted)";
    if (verdict === "SAFE") statusColor = "var(--accent-safe)";
    else if (verdict === "SUSPICIOUS") statusColor = "var(--accent-suspicious)";
    else if (verdict === "MALICIOUS") statusColor = "var(--accent-malicious)";

    const getLayerColor = (score) => {
        if (score >= 80) return 'var(--accent-safe)';
        if (score >= 50) return 'var(--accent-suspicious)';
        return 'var(--accent-malicious)';
    };

    return (
        <div style={{
            border: `1px solid ${statusColor}`,
            background: 'var(--bg-card)',
            padding: '2rem',
            marginTop: '2rem',
            boxShadow: `0 0 20px ${statusColor}22`
        }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                <h2 className="glitch-text" style={{ margin: 0, color: statusColor, fontSize: '2rem' }}>
                    VERDICT: {verdict}
                </h2>
                <div style={{ textAlign: 'right' }}>
                    <div style={{ fontSize: '3rem', fontWeight: 'bold', color: statusColor }}>
                        {safety_score}
                    </div>
                    <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>SAFETY SCORE</div>
                </div>
            </div>

            <div style={{ marginBottom: '2rem' }}>
                <div style={{
                    height: '4px',
                    width: '100%',
                    background: '#333',
                    position: 'relative'
                }}>
                    <div style={{
                        height: '100%',
                        width: `${safety_score}%`,
                        background: statusColor,
                        transition: 'width 1s ease-in-out',
                        boxShadow: `0 0 10px ${statusColor}`
                    }} />
                </div>
            </div>

            {layers && (
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1rem', marginBottom: '2rem' }}>
                    {Object.entries(layers).map(([key, data]) => (
                        <div key={key} style={{
                            background: 'var(--bg-secondary)',
                            padding: '1rem',
                            borderTop: `2px solid ${getLayerColor(data.score)}`
                        }}>
                            <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>
                                {key.replace('layer_', '').replace('_', ' ')}
                            </div>
                            <div style={{ fontSize: '1.2rem', fontWeight: 'bold', color: 'var(--text-primary)', margin: '0.5rem 0' }}>
                                {data.score}
                            </div>
                            <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                                {data.details && data.details[0]}
                            </div>
                        </div>
                    ))}
                </div>
            )}

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>
                <div>
                    <h3 style={{ borderBottom: '1px solid #333', paddingBottom: '0.5rem', color: 'var(--text-secondary)' }}>RISK FACTORS</h3>
                    <ul style={{ listStyle: 'none', padding: 0 }}>
                        {risk_breakdown.length > 0 ? (
                            risk_breakdown.map((risk, i) => (
                                <li key={i} style={{ color: 'var(--accent-malicious)', marginBottom: '0.5rem' }}>
                                    ⚠ {risk}
                                </li>
                            ))
                        ) : (
                            <li style={{ color: 'var(--accent-safe)' }}>✓ No specific risks detected</li>
                        )}
                    </ul>
                </div>

                <div>
                    <h3 style={{ borderBottom: '1px solid #333', paddingBottom: '0.5rem', color: 'var(--text-secondary)' }}>TECHNICAL SIGNALS</h3>
                    <ul style={{ listStyle: 'none', padding: 0, fontSize: '0.9rem', color: 'var(--text-muted)' }}>
                        <li>URL Length: <span style={{ color: 'var(--text-primary)' }}>{signals.url_length} chars</span></li>
                        <li>HTTPS: <span style={{ color: signals.has_https ? 'var(--accent-safe)' : 'var(--accent-malicious)' }}>{signals.has_https ? 'Yes' : 'No'}</span></li>
                        <li>IP Address: <span style={{ color: signals.has_ip ? 'var(--accent-malicious)' : 'var(--accent-safe)' }}>{signals.has_ip ? 'Yes' : 'No'}</span></li>
                        <li>TLD: <span style={{ color: 'var(--text-primary)' }}>.{signals.tld}</span></li>
                    </ul>
                </div>
            </div>
        </div>
    );
};

export default ResultCard;
