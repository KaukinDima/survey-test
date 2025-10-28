// src/composables/useApi.js
import axios from "axios";
import { API_BASE, API_HOST } from "@/const/uri";

export async function fetchCities() {
  const { data } = await axios.get(API_BASE.city);
  return data; // [{id,name,slug,feature}]
}

export async function fetchSurveys(quarter) {
  const { data } = await axios.get(API_BASE.survey, { params: { quarter } });
  return data; // [{id,title,quarter}]
}

export async function fetchSections(waveId) {
  const url = `${API_BASE.survey}sections/?wave=${waveId}`
  const res = await fetch(url)
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return await res.json()
}

export async function fetchSectionsByWaveCode(code) {
  const { data } = await axios.get(`${API_BASE.survey}sections/`, {
    params: { wave_code: code }
  })
  return data
}

export async function fetchSurveysByWaveCode(waveCode) {
  const url = new URL(`${API_HOST}/surveys/`);
  if (waveCode) url.searchParams.set("wave_code", waveCode);
  const res = await fetch(url.toString());
  if (!res.ok) throw new Error(`surveys HTTP ${res.status}`);
  return await res.json();
}

export async function searchQuestions({ surveyId, q }) {
  const url = new URL(`${API_HOST}/questions/`);
  if (surveyId) url.searchParams.set("survey_id", surveyId);
  if (q) url.searchParams.set("q", q);
  const res = await fetch(url.toString());
  if (!res.ok) throw new Error(`questions HTTP ${res.status}`);
  return await res.json();
}

export async function fetchGroupedQuestions(params = {}) {
  const { wave, survey_id, city } = params;
  const url = `${API_BASE.question}grouped/`;
  const res = await axios.get(url, { params: { wave, survey_id, city } });
  return res.data;
}

