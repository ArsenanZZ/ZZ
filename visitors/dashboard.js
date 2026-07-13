import { initializeApp, getApps } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-app.js";
import { collection, getFirestore, onSnapshot } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-firestore.js";

const firebaseConfig = {
  apiKey: "AIzaSyDn4ot0prM_xLajgH4vNE1ejN_Ir4cNBsM",
  authDomain: "zhennan-website-comments.firebaseapp.com",
  projectId: "zhennan-website-comments",
  appId: "1:1019165954961:web:6abb4bb8fb21d507edc030"
};

const formatter = new Intl.NumberFormat("en-US");
const totalViews = document.querySelector("[data-total-views]");
const totalDetail = document.querySelector("[data-total-detail]");
const storyCount = document.querySelector("[data-story-count]");
const topViews = document.querySelector("[data-top-views]");
const topTitle = document.querySelector("[data-top-title]");
const rankings = document.querySelector("[data-rankings]");
const activity = document.querySelector("[data-activity]");
const emptyRankings = document.querySelector("[data-empty-rankings]");
const emptyActivity = document.querySelector("[data-empty-activity]");
let locationRecords = [];

function setMapState(selector, message) {
  const state = document.querySelector(selector);
  if (state) state.textContent = message;
}

function styleMap(slot, type) {
  const svg = slot.querySelector("svg");
  if (!svg) return false;
  svg.removeAttribute("width");
  svg.removeAttribute("height");
  svg.setAttribute("preserveAspectRatio", "xMidYMid meet");
  if (type === "china") {
    svg.setAttribute("viewBox", "25 20 750 545");
    svg.querySelectorAll("circle").forEach(function (circle) {
      circle.style.display = "none";
    });
  }
  svg.querySelectorAll("rect").forEach(function (rect) {
    rect.setAttribute("fill", "#101619");
  });
  svg.querySelectorAll("text, image").forEach(function (node) {
    node.style.display = "none";
  });
  svg.querySelectorAll("path").forEach(function (path) {
    const id = path.id || "";
    const isRegion = type === "world" ? id.startsWith("wm_") : id.startsWith("cn_");
    path.setAttribute("fill", isRegion ? "#27373b" : "none");
    path.setAttribute("stroke", isRegion ? "rgba(220, 241, 236, .26)" : "rgba(220, 241, 236, .12)");
    path.setAttribute("stroke-width", ".7");
    path.setAttribute("vector-effect", "non-scaling-stroke");
    path.style.opacity = isRegion ? ".9" : ".4";
    path.style.pointerEvents = "none";
  });
  return true;
}

function svgViewBox(svg) {
  const values = (svg.getAttribute("viewBox") || "0 0 800 500").split(/\s+/).map(Number);
  return { x: values[0], y: values[1], width: values[2], height: values[3] };
}

function heatColor(views, maxViews) {
  const strength = Math.max(0, Math.min(1, views / Math.max(maxViews, 1)));
  const red = Math.round(95 + strength * 160);
  const green = Math.round(210 - strength * 105);
  return "rgb(" + red + "," + green + ",82)";
}

function renderHeatPoints(slot, points) {
  const svg = slot?.querySelector("svg");
  if (!svg) return false;
  svg.querySelector("[data-heat-layer]")?.remove();
  if (!points.length) return true;

  const namespace = "http://www.w3.org/2000/svg";
  const layer = document.createElementNS(namespace, "g");
  const maxViews = Math.max.apply(null, points.map(function (point) { return point.views; }));
  layer.setAttribute("data-heat-layer", "true");
  layer.setAttribute("pointer-events", "none");
  points.forEach(function (point) {
    const radius = 4 + Math.min(13, Math.sqrt(point.views || 1) * 3);
    const halo = document.createElementNS(namespace, "circle");
    halo.setAttribute("cx", point.x.toFixed(2));
    halo.setAttribute("cy", point.y.toFixed(2));
    halo.setAttribute("r", String(radius * 1.8));
    halo.setAttribute("fill", heatColor(point.views, maxViews));
    halo.setAttribute("fill-opacity", ".16");
    layer.appendChild(halo);

    const marker = document.createElementNS(namespace, "circle");
    marker.setAttribute("cx", point.x.toFixed(2));
    marker.setAttribute("cy", point.y.toFixed(2));
    marker.setAttribute("r", String(radius));
    marker.setAttribute("fill", heatColor(point.views, maxViews));
    marker.setAttribute("fill-opacity", ".88");
    marker.setAttribute("stroke", "rgba(255,255,255,.78)");
    marker.setAttribute("stroke-width", ".8");
    const label = document.createElementNS(namespace, "title");
    label.textContent = point.label + ": " + formatter.format(point.views) + " visits";
    marker.appendChild(label);
    layer.appendChild(marker);
  });
  svg.appendChild(layer);
  return true;
}

function setHeatState(selector, points) {
  if (!points.length) {
    setMapState(selector, "Awaiting location data");
    return;
  }
  const visits = points.reduce(function (sum, point) { return sum + point.views; }, 0);
  setMapState(selector, points.length + " locations | " + formatter.format(visits) + " visits");
}

function renderWorldHeat(records) {
  const slot = document.querySelector("[data-world-map]");
  const svg = slot?.querySelector("svg");
  if (!svg) return;
  const viewBox = svgViewBox(svg);
  const points = records.map(function (record) {
    return {
      x: viewBox.x + ((record.longitude + 180) / 360) * viewBox.width,
      y: viewBox.y + ((90 - record.latitude) / 180) * viewBox.height,
      views: record.views,
      label: [record.city, record.region, record.country].filter(Boolean).join(", ")
    };
  });
  renderHeatPoints(slot, points);
  setHeatState("[data-world-map-state]", points);
}

function renderChinaHeat(records) {
  const slot = document.querySelector("[data-china-map]");
  const points = records.filter(function (record) { return record.countryCode === "CN"; }).map(function (record) {
    return {
      x: (record.longitude - 70) * 11.8,
      y: (55 - record.latitude) * 15,
      views: record.views,
      label: [record.city, record.region, "China"].filter(Boolean).join(", ")
    };
  });
  if (!renderHeatPoints(slot, points)) return;
  setHeatState("[data-china-map-state]", points);
}

function renderUsHeat(records) {
  const slot = document.querySelector("[data-us-map]");
  if (!slot?._locationProjection) return;
  const points = records.filter(function (record) { return record.countryCode === "US"; }).map(function (record) {
    const projected = slot._locationProjection([record.longitude, record.latitude]);
    if (!projected) return null;
    return {
      x: projected[0],
      y: projected[1],
      views: record.views,
      label: [record.city, record.region, "United States"].filter(Boolean).join(", ")
    };
  }).filter(Boolean);
  renderHeatPoints(slot, points);
  setHeatState("[data-us-map-state]", points);
}

function renderHeatMaps(records) {
  renderWorldHeat(records);
  renderChinaHeat(records);
  renderUsHeat(records);
}

async function renderUsMap(slot, stateSelector) {
  setMapState(stateSelector, "Loading map");
  try {
    const modules = await Promise.all([
      import("https://cdn.jsdelivr.net/npm/d3-geo@3/+esm"),
      import("https://cdn.jsdelivr.net/npm/topojson-client@3/+esm")
    ]);
    const geo = modules[0];
    const topojson = modules[1];
    const response = await fetch("https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json");
    if (!response.ok) throw new Error("Could not load state boundaries");
    const topology = await response.json();
    const states = topojson.feature(topology, topology.objects.states);
    const projection = geo.geoAlbersUsa().fitExtent([[24, 20], [776, 480]], states);
    const path = geo.geoPath(projection);
    const svgNamespace = "http://www.w3.org/2000/svg";
    const svg = document.createElementNS(svgNamespace, "svg");
    svg.setAttribute("viewBox", "0 0 800 500");
    svg.setAttribute("preserveAspectRatio", "xMidYMid meet");
    svg.setAttribute("aria-hidden", "true");

    states.features.forEach(function (feature) {
      const shape = document.createElementNS(svgNamespace, "path");
      shape.setAttribute("d", path(feature));
      shape.setAttribute("data-state-id", feature.id);
      shape.setAttribute("fill", "#27373b");
      shape.setAttribute("stroke", "rgba(220, 241, 236, .26)");
      shape.setAttribute("stroke-width", ".7");
      shape.setAttribute("vector-effect", "non-scaling-stroke");
      svg.appendChild(shape);
    });

    const borders = document.createElementNS(svgNamespace, "path");
    borders.setAttribute("d", path(topojson.mesh(topology, topology.objects.states, function (a, b) { return a !== b; })));
    borders.setAttribute("fill", "none");
    borders.setAttribute("stroke", "rgba(220, 241, 236, .42)");
    borders.setAttribute("stroke-width", ".75");
    borders.setAttribute("vector-effect", "non-scaling-stroke");
    svg.appendChild(borders);
    slot._locationProjection = projection;
    slot.replaceChildren(svg);
    renderHeatMaps(locationRecords);
  } catch (error) {
    setMapState(stateSelector, "Map unavailable");
  }
}

function renderLocationMaps() {
  const mapDefinitions = [
    { type: "world", slot: document.querySelector("[data-world-map]"), state: "[data-world-map-state]", markup: typeof WORLD_MAP_SVG === "undefined" ? null : WORLD_MAP_SVG },
    { type: "china", slot: document.querySelector("[data-china-map]"), state: "[data-china-map-state]", markup: typeof CHINA_MAP_SVG === "undefined" ? null : CHINA_MAP_SVG }
  ];
  mapDefinitions.forEach(function (map) {
    if (!map.slot || !map.markup) {
      setMapState(map.state, "Map unavailable");
      return;
    }
    map.slot.innerHTML = map.markup;
    setMapState(map.state, styleMap(map.slot, map.type) ? "Awaiting location data" : "Map unavailable");
  });
  const usSlot = document.querySelector("[data-us-map]");
  if (usSlot) renderUsMap(usSlot, "[data-us-map-state]");
  renderHeatMaps(locationRecords);
}

function formatDate(value) {
  if (!value) return "No recent timestamp";
  return new Intl.DateTimeFormat("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric"
  }).format(value);
}

function escapeHtml(value) {
  return String(value || "").replace(/[&<>"']/g, function (char) {
    return ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" })[char];
  });
}

function renderRankings(stories) {
  if (!stories.length) {
    emptyRankings.classList.remove("hidden");
    return;
  }
  const largest = Math.max(stories[0].views, 1);
  rankings.innerHTML = stories.slice(0, 8).map(function (story) {
    const width = Math.max(5, Math.round((story.views / largest) * 100));
    return [
      '<div class="ranking">',
      '  <div>',
      '    <span class="ranking-title" title="' + escapeHtml(story.title) + '">' + escapeHtml(story.title) + "</span>",
      '    <div class="bar"><span class="bar-fill" style="width:' + width + '%"></span></div>',
      "  </div>",
      '  <span class="ranking-value">' + formatter.format(story.views) + "</span>",
      "</div>"
    ].join("");
  }).join("");
}

function renderActivity(stories) {
  const recent = stories.filter(function (story) { return story.updatedAt; }).slice(0, 6);
  if (!recent.length) {
    emptyActivity.classList.remove("hidden");
    return;
  }
  activity.innerHTML = recent.map(function (story) {
    return [
      '<div class="activity-item">',
      '  <span class="activity-title">' + escapeHtml(story.title) + "</span>",
      '  <span class="activity-meta">' + formatter.format(story.views) + " views | " + formatDate(story.updatedAt) + "</span>",
      "</div>"
    ].join("");
  }).join("");
}

function renderDashboard(snapshot) {
  const stories = snapshot.docs.map(function (doc) {
    const data = doc.data();
    return {
      title: data.title || data.path || "Untitled story",
      views: Number(data.views || 0),
      updatedAt: data.updatedAt?.toDate ? data.updatedAt.toDate() : null
    };
  });
  const byViews = stories.slice().sort(function (a, b) { return b.views - a.views; });
  const byRecent = stories.slice().sort(function (a, b) {
    return (b.updatedAt?.getTime() || 0) - (a.updatedAt?.getTime() || 0);
  });
  const views = byViews.reduce(function (sum, story) { return sum + story.views; }, 0);

  totalViews.textContent = formatter.format(views);
  totalDetail.textContent = stories.length ? "Across " + formatter.format(stories.length) + " tracked stories" : "No activity yet";
  storyCount.textContent = formatter.format(stories.length);
  topViews.textContent = byViews.length ? formatter.format(byViews[0].views) : "0";
  topTitle.textContent = byViews.length ? byViews[0].title : "No story yet";
  renderRankings(byViews);
  renderActivity(byRecent);
}

const app = getApps().length ? getApps()[0] : initializeApp(firebaseConfig);
const db = getFirestore(app);

window.addEventListener("load", function () {
  renderLocationMaps();
  onSnapshot(collection(db, "zzArticleStats"), function (snapshot) {
    renderDashboard(snapshot);
  }, function () {
    totalDetail.textContent = "Activity is temporarily unavailable.";
    emptyRankings.classList.remove("hidden");
    emptyActivity.classList.remove("hidden");
  });
  onSnapshot(collection(db, "zzVisitorLocations"), function (snapshot) {
    locationRecords = snapshot.docs.map(function (doc) {
      const data = doc.data();
      return {
        country: data.country || "",
        countryCode: data.countryCode || "",
        region: data.region || "",
        city: data.city || "",
        latitude: Number(data.latitude),
        longitude: Number(data.longitude),
        views: Number(data.views || 0)
      };
    }).filter(function (record) {
      return Number.isFinite(record.latitude) && Number.isFinite(record.longitude) && record.views > 0;
    });
    renderHeatMaps(locationRecords);
  }, function () {
    setMapState("[data-world-map-state]", "Location data unavailable");
    setMapState("[data-us-map-state]", "Location data unavailable");
    setMapState("[data-china-map-state]", "Location data unavailable");
  });
}, { once: true });
