import React, { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { Skeleton } from "@/components/ui/skeleton";

const storyTypes = [
  "Thrilling mysteries",
  "Heartwarming romances",
  "Epic adventures",
  "Thought-provoking dramas",
  "Inspiring true stories"
];

const readingMoods = [
  "Light and fun",
  "Emotional and deep",
  "Dark and intense",
  "Inspiring and uplifting",
  "Something else"
];

const pacingPreferences = [
  "Fast-paced",
  "Slow and immersive",
  "A mix of both"
];

const settings = [
  "Realistic modern-day",
  "Historical past",
  "Futuristic or sci-fi worlds",
  "Magical or fantastical lands"
];

const themes = [
  "Love & relationships",
  "Self-growth & mental health",
  "Adventure & survival",
  "Crime & mystery",
  "Science & technology",
  "Philosophy & life questions"
];

export default function BookRecommenderForm() {
  const [formData, setFormData] = useState({
    storyTypes: [],
    readingMoods: [],
    pacing: [],
    settings: [],
    themes: [],
    format: ""
  });

  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleCheckboxChange = (category, value) => {
    setFormData((prev) => {
      const updated = prev[category].includes(value)
        ? prev[category].filter((v) => v !== value)
        : [...prev[category], value];
      return { ...prev, [category]: updated };
    });
  };

  const handleSubmit = async () => {
    setLoading(true);
    setRecommendations([]);
    const response = await fetch("/api/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });
    const result = await response.json();
    setRecommendations(result.recommendations);
    setLoading(false);
  };

  return (
    <Card className="max-w-xl mx-auto p-6">
      <CardContent className="space-y-4">
        <h2 className="text-xl font-semibold">📚 Book Recommender</h2>

        <Label>1. What kind of stories do you enjoy most?</Label>
        <div className="flex flex-wrap gap-2">
          {storyTypes.map((s) => (
            <label key={s} className="flex items-center space-x-2">
              <Checkbox
                checked={formData.storyTypes.includes(s)}
                onCheckedChange={() => handleCheckboxChange("storyTypes", s)}
              />
              <span>{s}</span>
            </label>
          ))}
        </div>

        <Separator />

        <Label>2. Which of these best matches your current reading mood?</Label>
        <div className="flex flex-wrap gap-2">
          {readingMoods.map((m) => (
            <label key={m} className="flex items-center space-x-2">
              <Checkbox
                checked={formData.readingMoods.includes(m)}
                onCheckedChange={() => handleCheckboxChange("readingMoods", m)}
              />
              <span>{m}</span>
            </label>
          ))}
        </div>

        <Separator />

        <Label>3. Do you prefer fast-paced, action-packed plots or slower, more character-focused stories?</Label>
        <div className="flex flex-wrap gap-2">
          {pacingPreferences.map((p) => (
            <label key={p} className="flex items-center space-x-2">
              <Checkbox
                checked={formData.pacing.includes(p)}
                onCheckedChange={() => handleCheckboxChange("pacing", p)}
              />
              <span>{p}</span>
            </label>
          ))}
        </div>

        <Separator />

        <Label>4. What kind of settings do you enjoy most?</Label>
        <div className="flex flex-wrap gap-2">
          {settings.map((s) => (
            <label key={s} className="flex items-center space-x-2">
              <Checkbox
                checked={formData.settings.includes(s)}
                onCheckedChange={() => handleCheckboxChange("settings", s)}
              />
              <span>{s}</span>
            </label>
          ))}
        </div>

        <Separator />

        <Label>5. Which themes or topics interest you the most?</Label>
        <div className="flex flex-wrap gap-2">
          {themes.map((t) => (
            <label key={t} className="flex items-center space-x-2">
              <Checkbox
                checked={formData.themes.includes(t)}
                onCheckedChange={() => handleCheckboxChange("themes", t)}
              />
              <span>{t}</span>
            </label>
          ))}
        </div>

        <Separator />

        <Label>6. Do you like sticking to your favorite genres, or are you open to trying something new?</Label>
        <select
          value={formData.format}
          onChange={(e) => setFormData({ ...formData, format: e.target.value })}
          className="w-full p-2 border rounded"
        >
          <option value="">Select an option</option>
          <option value="Stick to favorites">Stick to favorites</option>
          <option value="Mix of both">Mix of both</option>
          <option value="Surprise me!">Surprise me!</option>
        </select>

        <Button className="mt-4 w-full" onClick={handleSubmit} disabled={loading}>
          {loading ? "🔄 Finding books..." : "🔍 Get Recommendations"}
        </Button>

        {loading && (
          <div className="space-y-2 mt-6">
            <Skeleton className="w-full h-6 rounded" />
            <Skeleton className="w-5/6 h-6 rounded" />
            <Skeleton className="w-3/4 h-6 rounded" />
          </div>
        )}

        {recommendations.length > 0 && (
          <div className="mt-6">
            <h3 className="text-lg font-semibold">📖 Recommended Books:</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-4">
              {recommendations.map((book, index) => (
                <div key={index} className="flex items-center space-x-4">
                  <img
                    src={`https://covers.openlibrary.org/b/isbn/${book.isbn}-M.jpg`}
                    alt={book.title}
                    className="w-16 h-24 object-cover rounded shadow"
                    onError={(e) => {
                      e.target.onerror = null;
                      e.target.src = "https://via.placeholder.com/100x150?text=No+Cover";
                    }}
                  />
                  <div>
                    <p className="font-medium">{book.title}</p>
                    <p className="text-sm text-gray-500">{book.author}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
