interface Props {
  confidence: number;
}

const LEVELS = [
  { min: 0.8, label: "High", color: "#16a34a" },
  { min: 0.5, label: "Medium", color: "#d97706" },
  { min: 0, label: "Low", color: "#dc2626" },
];

export function ConfidenceBadge({ confidence }: Props) {
  const level = LEVELS.find((l) => confidence >= l.min) ?? LEVELS[2];
  return (
    <span
      style={{
        display: "inline-block",
        padding: "2px 10px",
        borderRadius: 9999,
        fontSize: 12,
        fontWeight: 700,
        color: "#fff",
        background: level.color,
        letterSpacing: "0.04em",
      }}
    >
      {level.label} confidence ({Math.round(confidence * 100)}%)
    </span>
  );
}
