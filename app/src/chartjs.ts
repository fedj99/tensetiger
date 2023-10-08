/*
 * Registers all Chart JS components required for vue-chartjs to work
 */

import {
    BarElement,
    CategoryScale,
    Chart,
    Colors,
    Filler,
    Legend,
    LineElement,
    LinearScale,
    PointElement,
    TimeScale,
    Title,
    Tooltip,
} from "chart.js";
import "chartjs-adapter-luxon";
// import "chartjs-adapter-moment";

Chart.register(
    BarElement,
    CategoryScale,
    Legend,
    LineElement,
    LinearScale,
    PointElement,
    TimeScale,
    Title,
    Tooltip,
    Filler,
    Colors
);
