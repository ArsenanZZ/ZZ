// ==========================================
// BILINGUAL LANGUAGE DICTIONARY
// ==========================================

const translations = {
    zh: {
        valve: {
            title: "智能控制阀 (Control Valve Head)",
            desc: "被称为软水机的“大脑”。负责控制水流的方向，自动执行运行、反洗、吸盐、正洗和注水五大再生循环步骤。高品质的阀头能大幅提升软水机的使用寿命并节省水盐消耗。",
            specs: [
                "工作模式：时间控制、流量控制或双控制模式",
                "核心材质：高级工程塑料、无铅黄铜或工业陶瓷",
                "关键指标：最大出水流量、反洗频率与自动控制精度"
            ]
        },
        resinTank: {
            title: "玻璃钢树脂罐 (Resin Tank)",
            desc: "用于盛放离子交换树脂和中心管的耐压容器。通常由食品级PE内胆和无缝缠绕的玻璃纤维外壳组成，必须具备极强的耐压、防爆和防腐蚀性能。",
            specs: [
                "标准承压：通常不低于 100-150 psi (约10公斤水压)",
                "结构设计：底部配水器 + 中心集水管 + 上部配水器",
                "使用寿命：正常家庭使用可达 10 年以上"
            ]
        },
        brineTank: {
            title: "盐箱与盐井 (Brine Tank)",
            desc: "储存软水盐并配制饱和盐水（用于树脂再生）的容器。内置盐井、浮球阀以及吸盐限流阀，防止水流溢出，确保每次吸盐的配比准确。",
            specs: [
                "盐箱设计：干盐箱设计（平时无水，临再生前注水，防起拱）",
                "安全防护：双重防溢流浮球机构，溢流口防护",
                "维护频率：通常每 1-2 个月添加一次专用软水盐"
            ]
        },
        bypass: {
            title: "旁通阀 (Bypass Valve)",
            desc: "连接软水机与自来水管道的旁路切断装置。在机器维护、加盐或浇花不需要软水时，可通过手动旋钮将水流切换为直通自来水，无需关闭家中的主水阀。",
            specs: [
                "主要材质：高强度工程塑料 (Noryl) 或不锈钢",
                "操作模式：一键旋转切断，直观的三阀组功能集成",
                "安装便利：支持 360 度快速接头连接"
            ]
        },
        regen: {
            service: {
                badge: "阶段 1/5 - 正常运行 (Service)",
                title: "硬水软化过滤中",
                desc: "原水（硬水）从控制阀的进水口流入，自上而下通过树脂层。钙、镁硬度离子被树脂吸附并置换出等摩尔量的钠离子。软化后的水通过底部的布水器进入中心管，向上流出软水机，供给全屋使用。",
                statDuration: "常规工作状态",
                statFlow: "可达 1.5 - 3.5 吨/小时"
            },
            backwash: {
                badge: "阶段 2/5 - 反洗清洗 (Backwash)",
                title: "反向冲刷松动树脂层",
                desc: "控制阀改变水流方向，水流由中心管向下流到底部布水器，然后自下而上冲刷树脂层，并从阀头排污口排出。目的是为了使压实的树脂层松动，洗掉运行期间截留的泥沙、铁锈和破碎的树脂颗粒。",
                statDuration: "约 10 - 15 分钟",
                statFlow: "大流量排污"
            },
            brineDraw: {
                badge: "阶段 3/5 - 吸盐与慢洗 (Brine Draw & Slow Rinse)",
                title: "高浓度盐水置换还原",
                desc: "阀头利用文丘里喷射器产生的真空，将盐箱中的饱和盐水吸入树脂罐。高浓度的钠离子（Na⁺）冲刷树脂，把已经吸附的钙、镁离子置换出来，随废水从排污口排走。吸盐完毕后，清水继续慢速冲洗树脂，完成深层还原。",
                statDuration: "约 50 - 60 分钟",
                statFlow: "极微弱流速（高效浸泡）"
            },
            fastRinse: {
                badge: "阶段 4/5 - 正洗整理 (Fast Rinse)",
                title: "清除残留盐水分压实树脂",
                desc: "水流以正常运行的方向（自上而下）快速通过树脂层并直接排入排污管道。主要功能是冲洗掉树脂层中残留的盐水和硬度离子，并压实冲乱的树脂层，使其恢复到最佳的工作紧密状态。",
                statDuration: "约 8 - 12 分钟",
                statFlow: "额定设计流速"
            },
            refill: {
                badge: "阶段 5/5 - 盐箱注水 (Brine Refill)",
                title: "为下一次再生准备盐水",
                desc: "控制阀向盐箱中注入设计精密的淡水量，用于溶解食盐并配置下一次再生所需的饱和盐水。一般采用“干盐箱”设计的机器，会在此时将盐水备好，而高档机型则会采用临再生前数小时注水的方式，避免长期泡水滋生细菌。",
                statDuration: "约 5 - 10 分钟",
                statFlow: "小流速注水"
            }
        },
        radarLabels: ["性价比", "省水省盐", "寿命耐用", "智能化", "售后维护"],
        simStatus: {
            excellent: "树脂活性状态：<strong>优良</strong><br><span style='color:var(--text-secondary);font-size:13px'>硬水离子进入，被充分吸附，出水硬度趋于0。</span>",
            moderate: "树脂活性状态：<strong>中等饱和</strong><br><span style='color:var(--text-secondary);font-size:13px'>部分树脂已被钙镁覆盖，建议近期进行再生。</span>",
            exhausted: "树脂活性状态：<strong>完全饱和（失效）</strong><br><span style='color:var(--text-secondary);font-size:13px'>软水机已失去软化能力，必须注入饱和盐水进行清洗置换。</span>",
            regen: "树脂状态：<strong>高浓度盐水（Na⁺）冲刷中...</strong><br><span style='color:var(--text-secondary);font-size:13px'>钙镁离子被迫脱离树脂排向污水，钠离子重新附着在树脂表面。</span>"
        },
        simTitles: {
            softening: "离子置换软化模拟",
            regen: "食盐水冲刷再生模拟"
        },
        usHardnessDesc: {
            soft: "(软水：几乎无垢)",
            mod: "(中度硬水：常见水垢)",
            hard: "(重度硬水：水垢坚硬且多)",
            veryHard: "(极硬水：严重腐蚀涉水家电)"
        }
    },
    en: {
        valve: {
            title: "Smart Control Valve Head",
            desc: "Known as the 'Brain' of the water softener. It manages water flow direction and automatically executes the 5-stage regeneration cycle: Service, Backwash, Brine Draw, Fast Rinse, and Brine Refill. High-quality valves dramatically increase lifespan and minimize water and salt waste.",
            specs: [
                "Control Type: Time-based, Meter-based (Flow), or Dual Hybrid control",
                "Core Material: High-grade Noryl plastic, Lead-free Brass, or Industrial Ceramics",
                "Key Metrics: Max service flow rate, backwash frequency, and automatic dosing precision"
            ]
        },
        resinTank: {
            title: "FRP Resin Tank",
            desc: "A pressure vessel containing the ion exchange resin and the distributor riser pipe. Made of a food-grade PE liner wrapped with high-strength fiberglass, it must resist high water pressure and corrosion.",
            specs: [
                "Pressure Rating: Typically rated for at least 100-150 psi",
                "Internal Design: Bottom distributor basket + central riser tube + top basket",
                "Expected Lifespan: Exceeds 10 years under standard residential usage"
            ]
        },
        brineTank: {
            title: "Brine Tank & Brine Well",
            desc: "Holds the softener salt and prepares the saturated brine required for resin regeneration. It contains a brine well, air-check float safety valve, and draw controller to prevent water overflow.",
            specs: [
                "Salt System: Dry brine design (water only added prior to regeneration, preventing salt bridging)",
                "Safety System: Double safety float assembly with overflow elbow protection",
                "Maintenance: Refill with dedicated water softener salt pellets every 1-2 months"
            ]
        },
        bypass: {
            title: "Bypass Valve",
            desc: "A bypass manifold connecting the softener to the household main plumbing. It allows the water flow to bypass the softener for irrigation, maintenance, or refilling salt without shutting off the main home water line.",
            specs: [
                "Key Material: Reinforced engineering plastic (Noryl) or Stainless Steel",
                "Operation: Quick turn dial with fully integrated three-valve bypass logic",
                "Plumbing Fit: Supports 360-degree rotation quick-connect adapters"
            ]
        },
        regen: {
            service: {
                badge: "Stage 1/5 - Service (Softening)",
                title: "Hard Water Softening & Filtration",
                desc: "Raw hard water enters through the inlet valve and flows downward through the resin bed. Calcium and magnesium ions are captured by the resin, releasing sodium ions in their place. Soft water flows up the central riser pipe and exits to the house.",
                statDuration: "Continuous Service Mode",
                statFlow: "Up to 1.5 - 3.5 m³/h (6.6 - 15.4 GPM)"
            },
            backwash: {
                badge: "Stage 2/5 - Backwash",
                title: "Upward Flow to Loosen Resin Bed",
                desc: "The control valve reverses the water flow. Water goes down the riser tube and flows upward through the resin, flushing out dirt, silt, rust particles, and broken resin beads out through the drain port.",
                statDuration: "Approx. 10 - 15 mins",
                statFlow: "High flow drain rate"
            },
            brineDraw: {
                badge: "Stage 3/5 - Brine Draw & Slow Rinse",
                title: "Saturated Brine Ion Replacement",
                desc: "Using a Venturi injector, the valve draws saturated salt brine from the brine tank. The high concentration of Sodium (Na⁺) forces Calcium and Magnesium off the resin beads, discharging them down the drain. This is followed by a slow rinse to complete regeneration.",
                statDuration: "Approx. 50 - 60 mins",
                statFlow: "Extremely low flow (soak phase)"
            },
            fastRinse: {
                badge: "Stage 4/5 - Fast Rinse",
                title: "Flushing Leftover Brine & Compacting Bed",
                desc: "Water flows downward in the normal service direction and goes directly to the drain. This flushes out any remaining salty taste and hardness minerals, while settling and compacting the resin bed for optimal softening performance.",
                statDuration: "Approx. 8 - 12 mins",
                statFlow: "Standard service flow rate"
            },
            refill: {
                badge: "Stage 5/5 - Brine Refill",
                title: "Adding Water to Salt Tank",
                desc: "The control valve directs fresh water back into the brine tank to dissolve salt, preparing the saturated brine for the next regeneration cycle. Modern softeners refill at the end of the cycle (or hours before the next one) to prevent bacterial growth.",
                statDuration: "Approx. 5 - 10 mins",
                statFlow: "Low flow refill rate"
            }
        },
        radarLabels: ["Value/Cost", "Eco-Saving", "Durability", "Smart Tech", "Service"],
        simStatus: {
            excellent: "Resin Status: <strong>Excellent</strong><br><span style='color:var(--text-secondary);font-size:13px'>Hard water ions are fully captured. Exit hardness is near 0.</span>",
            moderate: "Resin Status: <strong>Moderate Saturation</strong><br><span style='color:var(--text-secondary);font-size:13px'>Part of the resin is covered by Ca/Mg. Regeneration recommended soon.</span>",
            exhausted: "Resin Status: <strong>Exhausted (100% Saturated)</strong><br><span style='color:var(--text-secondary);font-size:13px'>Softening capability lost. Brine wash regeneration is required immediately.</span>",
            regen: "Resin Status: <strong>Brine Wash (Na⁺ flushing)...</strong><br><span style='color:var(--text-secondary);font-size:13px'>Calcium/Magnesium are kicked off to drain. Sodium is attaching back to resin.</span>"
        },
        simTitles: {
            softening: "Ion Exchange Softening Simulation",
            regen: "Brine Regeneration Simulation"
        },
        usHardnessDesc: {
            soft: "(Soft: Very low scale)",
            mod: "(Moderately Hard: Scale occurs)",
            hard: "(Hard: Heavy white scale build-up)",
            veryHard: "(Very Hard: Severe appliance damage)"
        }
    }
};

let currentLang = 'en'; // Default language

function toggleLanguage() {
    currentLang = currentLang === 'zh' ? 'en' : 'zh';
    document.body.classList.toggle('lang-en', currentLang === 'en');

    // Update dynamically rendered components
    // 1. Re-render active Anatomy card
    const activeAnatomy = document.querySelector('.softener-schematic .active');
    if (activeAnatomy) {
        activeAnatomy.click();
    }

    // 2. Re-render active Regeneration card
    const activeRegen = document.querySelector('.regen-tabs .active');
    if (activeRegen) {
        activeRegen.click();
    }

    // 3. Update Canvas Texts (which are drawn on screen or display in DOM)
    // Update simulation status text
    const regenBtn = document.getElementById('btnRegenTrigger');
    const resetBtn = document.getElementById('btnResetCanvas');
    if (currentLang === 'en') {
        if(regenBtn) regenBtn.innerText = (simulationMode === 'softening') ? 'Manual Regeneration' : 'Restoring Resin...';
        if(resetBtn) resetBtn.innerText = 'Reset Simulator';
    } else {
        if(regenBtn) regenBtn.innerText = (simulationMode === 'softening') ? '手动启动再生冲洗' : '正在还原树脂...';
        if(resetBtn) resetBtn.innerText = '重置模拟器';
    }

    // 4. Redraw Brand Radar chart
    const activeBrand = document.querySelector('.brand-selector .active');
    const brandKey = activeBrand ? activeBrand.dataset.brand : 'ecowater';
    drawRadarChart(brandKey);
    updateBrandDetails(brandKey);

    // 5. Trigger calculation to update recommendation text in correct language
    const hardnessSlider = document.getElementById('calcHardness');
    if (hardnessSlider) {
        hardnessSlider.dispatchEvent(new Event('input'));
    } else {
        calculateResults();
    }
}

// Bind language toggle button
document.addEventListener('DOMContentLoaded', () => {
    const langBtn = document.getElementById('langToggleBtn');
    if (langBtn) {
        langBtn.addEventListener('click', toggleLanguage);
    }
});


// ==========================================
// 1. ANATOMY INTERACTIVE DISPLAY
// ==========================================

function initAnatomy() {
    const cards = document.querySelectorAll('.schematic-valve, .schematic-resin-tank, .schematic-brine-tank, .schematic-bypass-valve');
    const infoCard = document.getElementById('anatomyInfoCard');

    cards.forEach(card => {
        card.addEventListener('click', () => {
            cards.forEach(c => c.classList.remove('active'));
            card.classList.add('active');

            const key = card.dataset.part;
            const data = translations[currentLang][key];

            if (data) {
                let specsHtml = '';
                data.specs.forEach(spec => {
                    specsHtml += `<li>${spec}</li>`;
                });

                infoCard.innerHTML = `
                    <h3>${data.title}</h3>
                    <p>${data.desc}</p>
                    <ul class="anatomy-spec-list">
                        ${specsHtml}
                    </ul>
                `;
            }
        });
    });

    if(cards.length > 0) {
        cards[0].click();
    }
}

// ==========================================
// 2. REGENERATION FLOW STAGES CONTROL
// ==========================================

function initRegenTabs() {
    const tabs = document.querySelectorAll('.regen-tab-btn');
    const badge = document.getElementById('regenBadge');
    const title = document.getElementById('regenTitle');
    const desc = document.getElementById('regenDesc');
    const timeVal = document.getElementById('regenTimeVal');
    const flowVal = document.getElementById('regenFlowVal');

    const flowPaths = document.querySelectorAll('.flow-active-path');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            const stageKey = tab.dataset.stage;
            const data = translations[currentLang].regen[stageKey];

            if(data) {
                badge.innerText = data.badge;
                title.innerText = data.title;
                desc.innerText = data.desc;
                timeVal.innerText = data.statDuration;
                flowVal.innerText = data.statFlow;

                flowPaths.forEach(p => p.classList.remove('flow-active'));

                const activePath = document.getElementById(`path-${stageKey}`);
                if (activePath) activePath.classList.add('flow-active');
                const activePathOut = document.getElementById(`path-${stageKey}-out`);
                if (activePathOut) activePathOut.classList.add('flow-active');
                const activePathBrine = document.getElementById(`path-${stageKey}-brine`);
                if (activePathBrine) activePathBrine.classList.add('flow-active');
            }
        });
    });

    if(tabs.length > 0) {
        tabs[0].click();
    }
}

// ==========================================
// 3. CANVAS ION EXCHANGE SIMULATION
// ==========================================

let simulationMode = 'softening'; // shared
let saturationPercentage = 0;
let resins = [];
const floatingIons = [];
const RESIN_RADIUS = 36;
const ION_RADIUS = 7;
let canvas, ctx, animationFrameId;

function initIonExchangeSimulation() {
    canvas = document.getElementById('ionExchangeCanvas');
    if (!canvas) return;

    ctx = canvas.getContext('2d');

    function resizeCanvas() {
        canvas.width = canvas.parentElement.clientWidth;
        canvas.height = canvas.parentElement.clientHeight;
    }
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    const HARD_ION_SPAWN_CHANCE = 0.015;
    const NA_SPAWN_CHANCE = 0.05;

    class ResinBead {
        constructor(x, y) {
            this.x = x;
            this.y = y;
            this.capacity = 12;
            this.activeIons = [];
            this.init();
        }

        init() {
            this.activeIons = [];
            for (let i = 0; i < this.capacity; i++) {
                this.activeIons.push({
                    type: 'Na',
                    angle: (i / this.capacity) * Math.PI * 2,
                    distOffset: 0
                });
            }
        }

        draw() {
            const grad = ctx.createRadialGradient(this.x, this.y, 10, this.x, this.y, RESIN_RADIUS + 15);
            grad.addColorStop(0, 'rgba(251, 191, 36, 0.25)');
            grad.addColorStop(1, 'rgba(10, 15, 29, 0)');
            ctx.fillStyle = grad;
            ctx.beginPath();
            ctx.arc(this.x, this.y, RESIN_RADIUS + 15, 0, Math.PI * 2);
            ctx.fill();

            const bodyGrad = ctx.createRadialGradient(this.x - 5, this.y - 5, 5, this.x, this.y, RESIN_RADIUS);
            bodyGrad.addColorStop(0, '#fbbf24');
            bodyGrad.addColorStop(0.7, '#d97706');
            bodyGrad.addColorStop(1, '#78350f');
            ctx.fillStyle = bodyGrad;
            ctx.beginPath();
            ctx.arc(this.x, this.y, RESIN_RADIUS, 0, Math.PI * 2);
            ctx.fill();

            ctx.fillStyle = 'rgba(255, 255, 255, 0.4)';
            ctx.font = '10px sans-serif';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            for (let i = 0; i < 4; i++) {
                const r = RESIN_RADIUS * 0.4;
                const a = (i / 4) * Math.PI * 2 + 0.5;
                ctx.fillText('-', this.x + Math.cos(a) * r, this.y + Math.sin(a) * r);
            }

            this.activeIons.forEach(ion => {
                const ionX = this.x + Math.cos(ion.angle) * (RESIN_RADIUS + ion.distOffset);
                const ionY = this.y + Math.cos(ion.angle) * 0.1 + Math.sin(ion.angle) * (RESIN_RADIUS + ion.distOffset);

                if (ion.type === 'Na') {
                    ctx.fillStyle = '#38bdf8';
                    ctx.beginPath();
                    ctx.arc(ionX, ionY, ION_RADIUS - 1, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.fillStyle = '#0284c7';
                    ctx.beginPath();
                    ctx.arc(ionX, ionY, ION_RADIUS - 1, 0, Math.PI * 2, true);
                    ctx.stroke();
                } else {
                    ctx.fillStyle = '#ef4444';
                    ctx.beginPath();
                    ctx.arc(ionX, ionY, ION_RADIUS + 0.5, 0, Math.PI * 2);
                    ctx.fill();
                }
            });
        }

        getSaturation() {
            const hardCount = this.activeIons.filter(i => i.type === 'CaMg').length;
            return hardCount / this.capacity;
        }
    }

    function setupResins() {
        resins.length = 0;
        resins.push(new ResinBead(canvas.width * 0.35, canvas.height * 0.35));
        resins.push(new ResinBead(canvas.width * 0.65, canvas.height * 0.35));
        resins.push(new ResinBead(canvas.width * 0.25, canvas.height * 0.65));
        resins.push(new ResinBead(canvas.width * 0.55, canvas.height * 0.70));
    }
    setupResins();

    window.addEventListener('resize', () => {
        setupResins();
    });

    class FloatingIon {
        constructor(type) {
            this.type = type;
            this.x = Math.random() * canvas.width;
            this.y = (type === 'CaMg') ? -10 : canvas.height + 10;
            this.speedX = (Math.random() - 0.5) * 0.6;
            this.speedY = (type === 'CaMg') ? Math.random() * 1.5 + 1.2 : - (Math.random() * 1.5 + 1.2);
            this.released = false;
        }

        update() {
            this.x += this.speedX;
            this.y += this.speedY;

            if (this.x < 10 || this.x > canvas.width - 10) {
                this.speedX = -this.speedX;
            }
        }

        draw() {
            ctx.save();
            ctx.beginPath();
            ctx.arc(this.x, this.y, ION_RADIUS, 0, Math.PI * 2);

            if (this.type === 'CaMg') {
                const grad = ctx.createRadialGradient(this.x - 2, this.y - 2, 1, this.x, this.y, ION_RADIUS);
                grad.addColorStop(0, '#fca5a5');
                grad.addColorStop(0.8, '#ef4444');
                grad.addColorStop(1, '#b91c1c');
                ctx.fillStyle = grad;
                ctx.shadowColor = 'rgba(239, 68, 68, 0.4)';
                ctx.shadowBlur = 8;
                ctx.fill();

                ctx.fillStyle = '#ffffff';
                ctx.font = '7px sans-serif';
                ctx.fillText('Ca²', this.x - 3, this.y + 2.5);
            } else {
                const grad = ctx.createRadialGradient(this.x - 2, this.y - 2, 1, this.x, this.y, ION_RADIUS);
                grad.addColorStop(0, '#bae6fd');
                grad.addColorStop(0.8, '#38bdf8');
                grad.addColorStop(1, '#0284c7');
                ctx.fillStyle = grad;
                ctx.shadowColor = 'rgba(56, 189, 248, 0.4)';
                ctx.shadowBlur = 8;
                ctx.fill();

                ctx.fillStyle = '#ffffff';
                ctx.font = '7px sans-serif';
                ctx.fillText('Na', this.x - 2, this.y + 2.5);
            }
            ctx.restore();
        }
    }

    function updateSimulationUI() {
        const textElem = document.getElementById('simulationStatusText');
        const saturationBar = document.getElementById('saturationFill');
        const saturationNum = document.getElementById('saturationNum');
        const modeTitle = document.getElementById('simulationModeTitle');

        if(!textElem) return;

        let totalSat = 0;
        resins.forEach(r => totalSat += r.getSaturation());
        saturationPercentage = Math.round((totalSat / resins.length) * 100);

        saturationBar.style.width = `${saturationPercentage}%`;
        saturationNum.innerText = `${saturationPercentage}%`;

        const labels = translations[currentLang];

        if (simulationMode === 'softening') {
            modeTitle.innerText = labels.simTitles.softening;
            if (saturationPercentage < 40) {
                textElem.innerHTML = labels.simStatus.excellent;
                saturationBar.style.background = 'var(--accent-teal)';
            } else if (saturationPercentage < 90) {
                textElem.innerHTML = labels.simStatus.moderate;
                saturationBar.style.background = '#f59e0b';
            } else {
                textElem.innerHTML = labels.simStatus.exhausted;
                saturationBar.style.background = '#ef4444';
            }
        } else {
            modeTitle.innerText = labels.simTitles.regen;
            textElem.innerHTML = labels.simStatus.regen;
            saturationBar.style.background = 'var(--accent-blue)';
        }
    }

    function updateSim() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        if (simulationMode === 'softening') {
            if (Math.random() < HARD_ION_SPAWN_CHANCE && saturationPercentage < 100) {
                floatingIons.push(new FloatingIon('CaMg'));
            }
        } else {
            if (Math.random() < NA_SPAWN_CHANCE) {
                const na = new FloatingIon('Na');
                na.y = -10;
                na.speedY = Math.random() * 2 + 1.8;
                floatingIons.push(na);
            }
        }

        for (let i = floatingIons.length - 1; i >= 0; i--) {
            const ion = floatingIons[i];
            ion.update();
            ion.draw();

            let hitResin = false;
            for (let j = 0; j < resins.length; j++) {
                const resin = resins[j];
                const dx = ion.x - resin.x;
                const dy = ion.y - resin.y;
                const dist = Math.sqrt(dx*dx + dy*dy);

                if (dist < RESIN_RADIUS + 8) {
                    if (simulationMode === 'softening' && ion.type === 'CaMg' && !ion.released) {
                        const naIndex = resin.activeIons.findIndex(atom => atom.type === 'Na');
                        if (naIndex !== -1) {
                            resin.activeIons[naIndex].type = 'CaMg';

                            const releasedNa = new FloatingIon('Na');
                            releasedNa.x = ion.x;
                            releasedNa.y = ion.y;
                            releasedNa.speedY = Math.abs(ion.speedY) * 1.1;
                            releasedNa.released = true;
                            floatingIons.push(releasedNa);

                            floatingIons.splice(i, 1);
                            hitResin = true;
                            updateSimulationUI();
                            break;
                        }
                    } else if (simulationMode === 'regenerating' && ion.type === 'Na' && !ion.released) {
                        const caIndex = resin.activeIons.findIndex(atom => atom.type === 'CaMg');
                        if (caIndex !== -1) {
                            resin.activeIons[caIndex].type = 'Na';

                            const releasedCa = new FloatingIon('CaMg');
                            releasedCa.x = ion.x;
                            releasedCa.y = ion.y;
                            releasedCa.speedY = Math.abs(ion.speedY) * 1.2;
                            releasedCa.released = true;
                            floatingIons.push(releasedCa);

                            floatingIons.splice(i, 1);
                            hitResin = true;
                            updateSimulationUI();
                            break;
                        }
                    }
                }
            }

            if (hitResin) continue;

            if (ion.y > canvas.height + 20 || ion.y < -20) {
                floatingIons.splice(i, 1);
            }
        }

        resins.forEach(resin => resin.draw());

        if (simulationMode === 'regenerating') {
            let totalHardIons = 0;
            resins.forEach(r => {
                totalHardIons += r.activeIons.filter(atom => atom.type === 'CaMg').length;
            });
            if (totalHardIons === 0) {
                simulationMode = 'softening';
                const regenBtn = document.getElementById('btnRegenTrigger');
                if (regenBtn) {
                    regenBtn.innerText = currentLang === 'en' ? 'Manual Regeneration' : '手动启动再生冲洗';
                    regenBtn.classList.remove('btn-primary');
                    regenBtn.classList.add('btn-secondary');
                }
                updateSimulationUI();
            }
        }

        animationFrameId = requestAnimationFrame(updateSim);
    }

    const regenBtn = document.getElementById('btnRegenTrigger');
    if(regenBtn) {
        regenBtn.addEventListener('click', () => {
            if (simulationMode === 'softening') {
                simulationMode = 'regenerating';
                regenBtn.innerText = currentLang === 'en' ? 'Restoring Resin...' : '正在还原树脂...';
                regenBtn.classList.remove('btn-secondary');
                regenBtn.classList.add('btn-primary');
            } else {
                simulationMode = 'softening';
                regenBtn.innerText = currentLang === 'en' ? 'Manual Regeneration' : '手动启动再生冲洗';
                regenBtn.classList.remove('btn-primary');
                regenBtn.classList.add('btn-secondary');
            }
            updateSimulationUI();
        });
    }

    const resetBtn = document.getElementById('btnResetCanvas');
    if(resetBtn) {
        resetBtn.addEventListener('click', () => {
            resins.forEach(r => r.init());
            floatingIons.length = 0;
            simulationMode = 'softening';
            if (regenBtn) {
                regenBtn.innerText = currentLang === 'en' ? 'Manual Regeneration' : '手动启动再生冲洗';
                regenBtn.classList.remove('btn-primary');
                regenBtn.classList.add('btn-secondary');
            }
            updateSimulationUI();
        });
    }

    updateSim();
    updateSimulationUI();
}

// ==========================================
// 4. SVG RADAR CHART DRAWING
// ==========================================

const brandsData = {
    ecowater: {
        zh: {
            name: "美国怡口 (EcoWater)",
            label: "旗舰高端代表",
            desc: "怡口是软水机的鼻祖。在盘式阀技术、逆流再生（干盐箱）技术上处于行业绝对垄断地位，节水节盐高达30%。智能化程度高，寿命可达15-20年，但初始购入成本极高。旗下核心系列包括ERR系列（双罐活性炭结合软水）和HE系列（高效软水机）。",
            price: "12,000 - 35,000 元",
            tech: "自研多路旋转盘式阀 + 逆流干盐箱",
            cons: "滤料及配件更换较贵，二线城市售后代理水平不一。"
        },
        en: {
            name: "EcoWater (US)",
            label: "Flagship Luxury",
            desc: "EcoWater is the inventor of the water softener. Holding proprietary patents in rotary disc valves and counter-current (dry brine) technology, saving up to 30% water and salt. Lifespan reaches 15-20 years with premium smart home integration. Signature models: ERR (Softener+Refiner) and HE series.",
            price: "$1,800 - $5,000 USD",
            tech: "Proprietary Rotary Disc Valve + Upflow Dry Brine",
            cons: "High filter/resin replacement costs, dealer-locked service network."
        },
        color: "#3b82f6",
        score: [6, 9, 9, 9, 8] // Value/Cost, Eco-Saving, Durability, Smart Tech, Service
    },
    bwt: {
        zh: {
            name: "德国倍世 (BWT)",
            label: "欧系轻奢风范",
            desc: "欧洲水处理巨头。特色在于极富现代美感的设计和欧洲制造的高纯度食品级树脂。带有防菌镀银网设计，注重水质的无菌卫生。智能化水质监测出色，价格昂贵。主推Aquadial与Perla系列。",
            price: "15,000 - 40,000 元",
            tech: "Hygienic 镀银树脂抗菌技术 + 智能液晶多路阀",
            cons: "通量相对于同体积的美系软水机略小，对中国北方极硬水质耐受力一般。"
        },
        en: {
            name: "BWT (Germany)",
            label: "European Premium",
            desc: "European water treatment giant. Known for compact, ultra-modern luxury design and premium food-grade resins. Features unique silver-ion anti-bacterial tech. High smart automation. Highly popular models include Perla and Aquadial series.",
            price: "$2,200 - $6,000 USD",
            tech: "Hygienic Bio-Silver Resin + LCD Multi-port Valve",
            cons: "Lower flow rate per volume compared to US brands; sensitive to extremely hard water."
        },
        color: "#ec4899",
        score: [5, 8, 8, 9, 9]
    },
    runxin: {
        zh: {
            name: "润新 / 开能 (Runxin/Canature)",
            label: "高性价比国民选择",
            desc: "代表了国货的最高工业水平。润新控制阀以独创的“端面密封陶瓷阀芯”闻名全球，耐磨损损耐沙石，寿命极长。开能是中国最大的软水整机制造OEM厂商，整机质量极其扎实，出口北美各大市场。",
            price: "3,000 - 8,000 元",
            tech: "润新专利陶瓷端面密封阀 + 全自动流量型再生",
            cons: "机器颜值与美系、德系品牌有一定差距，数码面板操作逻辑较生硬。"
        },
        en: {
            name: "Runxin / Canature (China)",
            label: "Best Cost-Benefit",
            desc: "Represents the highest level of industrial water technology in China. Runxin control valves are globally famous for their patented ceramic disc flat seal, which resists grit/sand abrasion. Canature is a major global OEM manufacturer, providing solid build quality.",
            price: "$500 - $1,200 USD",
            tech: "Patented Ceramic Hermetic Valve + Metered Regeneration",
            cons: "Industrial/basic exterior design; LCD panel programming is less intuitive."
        },
        color: "#10b981",
        score: [9, 7, 8, 6, 7]
    },
    honeywell: {
        zh: {
            name: "3M / 霍尼韦尔 (Honeywell)",
            label: "品质家电大牌",
            desc: "两家跨国综合巨头在净水领域的产品。主要通过贴牌定制，或选用经典的美国富莱克阀头、润新阀头，搭配自家的品牌机壳。优势在于售后服务网络极其庞大，大品牌售后更有保障。",
            price: "6,000 - 12,000 元",
            tech: "OEM定制阀（富莱克/润新）+ 模块化机身设计",
            cons: "性价比一般，技术迭代较慢，软水核心科技缺乏壁垒。"
        },
        en: {
            name: "3M / Honeywell (US)",
            label: "Trusted Household Brands",
            desc: "These multi-national conglomerates license water softeners using standard OEM valve heads (like Fleck or Runxin) packaged in branded cabinets. The primary advantage is their vast retail distribution and excellent post-sales support networks.",
            price: "$900 - $2,000 USD",
            tech: "OEM Customized Valves (Fleck/Runxin) + Compact Cabinets",
            cons: "Average value for money; slower technological updates; lack of unique softening patents."
        },
        color: "#f59e0b",
        score: [7, 6, 7, 7, 8]
    }
};

function drawRadarChart(activeBrandKey = 'ecowater') {
    const svg = document.getElementById('brandRadarChart');
    if (!svg) return;

    svg.innerHTML = '';

    const width = 360;
    const height = 360;
    const cx = width / 2;
    const cy = height / 2;
    const rMax = 115;

    svg.setAttribute('viewBox', `0 0 ${width} ${height}`);

    function getCoords(index, value, maxVal = 10) {
        const angle = (index / 5) * Math.PI * 2 - Math.PI / 2;
        const radius = (value / maxVal) * rMax;
        return {
            x: cx + radius * Math.cos(angle),
            y: cy + radius * Math.sin(angle)
        };
    }

    const labels = translations[currentLang].radarLabels;

    // 1. Draw web grid
    for (let level = 2; level <= 10; level += 2) {
        let points = [];
        for (let i = 0; i < 5; i++) {
            const pt = getCoords(i, level);
            points.push(`${pt.x},${pt.y}`);
        }
        const polygon = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
        polygon.setAttribute('points', points.join(' '));
        polygon.setAttribute('fill', 'none');
        polygon.setAttribute('stroke', 'rgba(255, 255, 255, 0.08)');
        polygon.setAttribute('stroke-width', '1');
        svg.appendChild(polygon);

        if (level === 10) {
            const pt = getCoords(0, level);
            const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
            text.setAttribute('x', pt.x + 8);
            text.setAttribute('y', pt.y + 4);
            text.setAttribute('fill', 'var(--text-muted)');
            text.setAttribute('font-size', '9px');
            text.textContent = '10';
            svg.appendChild(text);
        }
    }

    // 2. Draw axis lines
    for (let i = 0; i < 5; i++) {
        const pt = getCoords(i, 10);
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttribute('x1', cx);
        line.setAttribute('y1', cy);
        line.setAttribute('x2', pt.x);
        line.setAttribute('y2', pt.y);
        line.setAttribute('stroke', 'rgba(255, 255, 255, 0.12)');
        line.setAttribute('stroke-width', '1.2');
        svg.appendChild(line);

        const textPt = getCoords(i, 11.6);
        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.setAttribute('x', textPt.x);
        text.setAttribute('y', textPt.y + 4);
        text.setAttribute('fill', 'var(--text-secondary)');
        text.setAttribute('font-size', '11px');
        text.setAttribute('font-weight', '600');
        text.setAttribute('text-anchor', 'middle');
        text.textContent = labels[i];
        svg.appendChild(text);
    }

    // 3. Inactive polygons
    Object.keys(brandsData).forEach(key => {
        if(key === activeBrandKey) return;

        const brand = brandsData[key];
        let points = [];
        for (let i = 0; i < 5; i++) {
            const pt = getCoords(i, brand.score[i]);
            points.push(`${pt.x},${pt.y}`);
        }

        const polygon = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
        polygon.setAttribute('points', points.join(' '));
        polygon.setAttribute('fill', brand.color);
        polygon.setAttribute('fill-opacity', '0.03');
        polygon.setAttribute('stroke', brand.color);
        polygon.setAttribute('stroke-width', '1');
        polygon.setAttribute('stroke-opacity', '0.2');
        polygon.setAttribute('stroke-dasharray', '3, 3');
        svg.appendChild(polygon);
    });

    // 4. Active Polygon
    const activeBrand = brandsData[activeBrandKey];
    if(activeBrand) {
        let points = [];
        for (let i = 0; i < 5; i++) {
            const pt = getCoords(i, activeBrand.score[i]);
            points.push(`${pt.x},${pt.y}`);
        }

        const polygon = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
        polygon.setAttribute('points', points.join(' '));
        polygon.setAttribute('fill', activeBrand.color);
        polygon.setAttribute('fill-opacity', '0.28');
        polygon.setAttribute('stroke', activeBrand.color);
        polygon.setAttribute('stroke-width', '2.5');
        polygon.setAttribute('filter', 'drop-shadow(0px 0px 8px ' + activeBrand.color + ')');
        svg.appendChild(polygon);

        for (let i = 0; i < 5; i++) {
            const pt = getCoords(i, activeBrand.score[i]);
            const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
            circle.setAttribute('cx', pt.x);
            circle.setAttribute('cy', pt.y);
            circle.setAttribute('r', '5');
            circle.setAttribute('fill', '#ffffff');
            circle.setAttribute('stroke', activeBrand.color);
            circle.setAttribute('stroke-width', '2.5');
            svg.appendChild(circle);

            const valText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
            valText.setAttribute('x', pt.x);
            valText.setAttribute('y', pt.y - 8);
            valText.setAttribute('fill', '#ffffff');
            valText.setAttribute('font-size', '10px');
            valText.setAttribute('font-weight', '700');
            valText.setAttribute('text-anchor', 'middle');
            valText.textContent = activeBrand.score[i];
            svg.appendChild(valText);
        }
    }
}

function updateBrandDetails(brandKey) {
    const data = brandsData[brandKey];
    if(!data) return;

    const brandLang = data[currentLang];

    document.getElementById('brandName').innerText = brandLang.name;
    document.getElementById('brandLabel').innerText = brandLang.label;
    document.getElementById('brandPrice').innerText = brandLang.price;
    document.getElementById('brandTech').innerText = brandLang.tech;
    document.getElementById('brandCons').innerText = brandLang.cons;
    document.getElementById('brandDesc').innerText = brandLang.desc;

    const detailsBox = document.getElementById('brandDetailsBox');
    detailsBox.style.borderColor = data.color + '40';
}

function initBrandSelector() {
    const cards = document.querySelectorAll('.brand-card-small');
    cards.forEach(card => {
        card.addEventListener('click', () => {
            cards.forEach(c => c.classList.remove('active'));
            card.classList.add('active');

            const brandKey = card.dataset.brand;
            drawRadarChart(brandKey);
            updateBrandDetails(brandKey);
        });
    });

    if(cards.length > 0) {
        cards[0].click();
    }
}

// ==========================================
// 5. BUYING ADVISOR CALCULATOR
// ==========================================

function initCalculator() {
    const hardnessSlider = document.getElementById('calcHardness');
    const hardnessVal = document.getElementById('hardnessVal');
    const hardnessDesc = document.getElementById('hardnessDesc');

    const familySlider = document.getElementById('calcFamily');
    const familyVal = document.getElementById('familyVal');

    const budgetCards = document.querySelectorAll('.calc-form .radio-card');
    let selectedBudget = 'quality';

    // Hardness change
    hardnessSlider.addEventListener('input', (e) => {
        const val = parseInt(e.target.value);
        hardnessVal.innerText = val;

        const labels = translations[currentLang].usHardnessDesc;

        if (val < 150) {
            hardnessDesc.innerText = labels.soft;
            hardnessDesc.style.color = "var(--accent-teal)";
        } else if (val < 300) {
            hardnessDesc.innerText = labels.mod;
            hardnessDesc.style.color = "var(--accent-blue)";
        } else if (val < 450) {
            hardnessDesc.innerText = labels.hard;
            hardnessDesc.style.color = "#f59e0b";
        } else {
            hardnessDesc.innerText = labels.veryHard;
            hardnessDesc.style.color = "#ef4444";
        }

        // Sync US GPG text in calculator if visible
        const gpgOutput = document.getElementById('calcHardnessGpgVal');
        if (gpgOutput) {
            gpgOutput.innerText = (val / 17.1).toFixed(1);
        }

        calculateResults();
    });

    // Family Size change
    familySlider.addEventListener('input', (e) => {
        familyVal.innerText = e.target.value;
        calculateResults();
    });

    // Budget Level cards click
    budgetCards.forEach(card => {
        card.addEventListener('click', () => {
            budgetCards.forEach(c => c.classList.remove('active'));
            card.classList.add('active');
            selectedBudget = card.dataset.budget;
            calculateResults();
        });
    });

    // Preset location links click
    const presetLinks = document.querySelectorAll('.preset-hardness-btn');
    presetLinks.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const ppm = parseInt(btn.dataset.ppm);
            hardnessSlider.value = ppm;
            // dispatch input event
            hardnessSlider.dispatchEvent(new Event('input'));
        });
    });

    // Initial sync
    hardnessSlider.dispatchEvent(new Event('input'));
}

// Global calculate results function so toggleLanguage can invoke it
function calculateResults() {
    const hardnessSlider = document.getElementById('calcHardness');
    const familySlider = document.getElementById('calcFamily');
    if (!hardnessSlider || !familySlider) return;

    const hardness = parseInt(hardnessSlider.value);
    const familySize = parseInt(familySlider.value);

    // Get active budget card
    const activeBudgetCard = document.querySelector('.calc-form .radio-card.active');
    const selectedBudget = activeBudgetCard ? activeBudgetCard.dataset.budget : 'quality';

    const dailySoftWaterLiters = familySize * 150;
    const dailyHardnessGrams = (hardness * dailySoftWaterLiters) / 1000;

    const targetCycleDays = 3.5;
    const requiredResinCapacityGrams = dailyHardnessGrams * targetCycleDays;
    const resinCapacityPerLiter = 45;
    let recommendedResinVolume = requiredResinCapacityGrams / resinCapacityPerLiter;

    if (recommendedResinVolume < 10) recommendedResinVolume = 10;
    else if (recommendedResinVolume < 15) recommendedResinVolume = 15;
    else if (recommendedResinVolume < 20) recommendedResinVolume = 20;
    else if (recommendedResinVolume < 25) recommendedResinVolume = 25;
    else if (recommendedResinVolume < 30) recommendedResinVolume = 30;
    else recommendedResinVolume = Math.ceil(recommendedResinVolume / 10) * 10;

    let recommendedFlowRate = 1.0;
    if (familySize <= 2) recommendedFlowRate = 1.0;
    else if (familySize <= 4) recommendedFlowRate = 1.5;
    else if (familySize <= 6) recommendedFlowRate = 2.0;
    else recommendedFlowRate = 2.5;

    const regenerationsPerYear = 365 / targetCycleDays;
    const annualSaltKg = Math.round((recommendedResinVolume * 0.12 * regenerationsPerYear));
    const annualWaterTons = Math.round((recommendedResinVolume * 8 * regenerationsPerYear) / 1000 * 10) / 10;

    // Water hardness in grains for US sizing references (Grains of capacity)
    // 1 grain = 17.1 ppm. Standard softeners are sized in Grains: 24,000 / 32,000 / 48,000 / 64,000 capacity.
    const hardnessGrainsCapacity = Math.round(recommendedResinVolume * resinCapacityPerLiter * 15.43); // 1g = 15.43 grains
    let standardGrainRating = 32000;
    if(hardnessGrainsCapacity < 24000) standardGrainRating = 24000;
    else if(hardnessGrainsCapacity <= 32000) standardGrainRating = 32000;
    else if(hardnessGrainsCapacity <= 48000) standardGrainRating = 48000;
    else if(hardnessGrainsCapacity <= 64000) standardGrainRating = 64000;
    else standardGrainRating = 80000;

    let recommendedValve = "";
    let recommendedBrand = "";
    let estimatedPrice = "";

    if (currentLang === 'zh') {
        if (selectedBudget === 'economy') {
            recommendedValve = "润新全自动陶瓷多路阀 (Runxin)";
            recommendedBrand = "开能 (Canature) / 润新整机";
            estimatedPrice = `${Math.round(recommendedResinVolume * 220 + 1200)} 元`;
        } else if (selectedBudget === 'quality') {
            recommendedValve = "富莱克 (Fleck 5600/6700) 活塞阀";
            recommendedBrand = "3M / 霍尼韦尔 (Honeywell) / 美的";
            estimatedPrice = `${Math.round(recommendedResinVolume * 300 + 3500)} 元`;
        } else {
            recommendedValve = "克莱克 (Clack EE/EI) 盘式阀 / 怡口自研阀";
            recommendedBrand = "美国怡口 (EcoWater) / 德国倍世 (BWT)";
            estimatedPrice = `${Math.round(recommendedResinVolume * 600 + 8000)} 元`;
        }
    } else {
        // English recommendations
        if (selectedBudget === 'economy') {
            recommendedValve = "Runxin Auto Ceramic Rotary Valve";
            recommendedBrand = "Canature OEM / Runxin cabinets";
            estimatedPrice = `$500 - $900 USD`;
        } else if (selectedBudget === 'quality') {
            recommendedValve = "Fleck 5600SXT / 6700 Downflow Piston Valve";
            recommendedBrand = "Pentair / 3M / Whirlpool Systems";
            estimatedPrice = `$900 - $1,600 USD`;
        } else {
            recommendedValve = "Clack WS1 Rotary Plate / EcoWater Disc Valve";
            recommendedBrand = "EcoWater Systems / BWT Luxury Series";
            estimatedPrice = `$1,800 - $4,200 USD`;
        }
    }

    // Standard metric updates
    document.getElementById('resFlowRate').innerHTML = `${recommendedFlowRate} <span>m³/h</span>`;
    document.getElementById('resResinVol').innerHTML = `${recommendedResinVolume} <span>L</span>`;
    document.getElementById('resAnnualSalt').innerHTML = `${annualSaltKg} <span>kg</span>`;
    document.getElementById('resAnnualWater').innerHTML = `${annualWaterTons} <span>${currentLang === 'en' ? 'Tons' : '吨'}</span>`;

    // US spec units mapping (displays in english mode or subtext)
    const gpm = (recommendedFlowRate * 4.403).toFixed(1);
    const grainsUnit = (standardGrainRating / 1000) + "k Grains";
    const saltLbs = Math.round(annualSaltKg * 2.205);
    const waterGal = Math.round(annualWaterTons * 264.17);

    const usFlowUnit = document.getElementById('resFlowRateUS');
    const usResinUnit = document.getElementById('resResinVolUS');
    const usSaltUnit = document.getElementById('resAnnualSaltUS');
    const usWaterUnit = document.getElementById('resAnnualWaterUS');

    if(usFlowUnit) usFlowUnit.innerText = `(${gpm} GPM)`;
    if(usResinUnit) usResinUnit.innerText = `(${grainsUnit})`;
    if(usSaltUnit) usSaltUnit.innerText = `(${saltLbs} lbs)`;
    if(usWaterUnit) usWaterUnit.innerText = `(${waterGal} Gal)`;

    document.getElementById('recValve').innerText = recommendedValve;
    document.getElementById('recBrand').innerText = recommendedBrand;
    document.getElementById('recPrice').innerText = estimatedPrice;
}

// ==========================================
// 6. GPG ↔ PPM CONVERTER PANEL
// ==========================================
function initGpgConverter() {
    const inputPpm = document.getElementById('convPpm');
    const inputGpg = document.getElementById('convGpg');

    if(!inputPpm || !inputGpg) return;

    inputPpm.addEventListener('input', (e) => {
        const val = parseFloat(e.target.value);
        if (isNaN(val)) {
            inputGpg.value = '';
        } else {
            inputGpg.value = (val / 17.12).toFixed(2);
        }
    });

    inputGpg.addEventListener('input', (e) => {
        const val = parseFloat(e.target.value);
        if (isNaN(val)) {
            inputPpm.value = '';
        } else {
            inputPpm.value = Math.round(val * 17.12);
        }
    });

    // Preset values initially
    inputPpm.value = 250;
    inputGpg.value = (250 / 17.12).toFixed(2);
}

// ==========================================
// 7. VALVE HEAD INTERNAL MECHANICS SIMULATOR
// ==========================================
function initValveSimulator() {
    const btnMechPiston = document.getElementById('btnMechPiston');
    const btnMechDisc = document.getElementById('btnMechDisc');
    const svgPistonSim = document.getElementById('svgPistonSim');
    const svgDiscSim = document.getElementById('svgDiscSim');

    const cycleBtns = document.querySelectorAll('.sim-cycle-btn');
    const valveSlider = document.getElementById('simValveSlider');
    const sliderValText = document.getElementById('simSliderValText');
    const lblSimCtrlSlider = document.getElementById('lblSimCtrlSlider');
    const lblSimCtrlSliderEn = document.getElementById('lblSimCtrlSliderEn');

    const pistonGroup = document.getElementById('gSimPiston');
    const discGroup = document.getElementById('gSimDisc');

    if (!btnMechPiston || !btnMechDisc) return;

    let currentMech = 'piston'; // 'piston' or 'disc'
    let currentSimStage = 'service';

    // Preset slider positions (0-100) or rotation angles (0-360)
    const pistonPresets = {
        service: 0,
        backwash: 25,
        brineDraw: 50,
        fastRinse: 75,
        refill: 100
    };

    const discPresets = {
        service: 0,
        backwash: 72,
        brineDraw: 144,
        fastRinse: 216,
        refill: 288
    };

    function updateFlowPaths(type, val) {
        // Clear active flow classes
        const allPaths = document.querySelectorAll('.sim-flow-path-internal');
        allPaths.forEach(p => p.classList.remove('flow-active'));

        if (type === 'piston') {
            // Map 0-100% to Y stroke offset (0 to 30px is a good range for SVG translation)
            const yOffset = (val / 100) * 35;
            pistonGroup.setAttribute('transform', `translate(0, ${yOffset})`);

            // Check proximity to activate paths
            const tol = 6;
            if (Math.abs(val - pistonPresets.service) <= tol) {
                const p = document.getElementById('p-path-service');
                if (p) p.classList.add('flow-active');
            } else if (Math.abs(val - pistonPresets.backwash) <= tol) {
                const p = document.getElementById('p-path-backwash');
                if (p) p.classList.add('flow-active');
            } else if (Math.abs(val - pistonPresets.brineDraw) <= tol) {
                const p = document.getElementById('p-path-brineDraw');
                if (p) p.classList.add('flow-active');
            } else if (Math.abs(val - pistonPresets.fastRinse) <= tol) {
                const p = document.getElementById('p-path-fastRinse');
                if (p) p.classList.add('flow-active');
            } else if (Math.abs(val - pistonPresets.refill) <= tol) {
                const p = document.getElementById('p-path-refill');
                if (p) p.classList.add('flow-active');
            }
        } else {
            // Map 0-100% to 0-360 degrees
            const angle = Math.round((val / 100) * 360);
            discGroup.setAttribute('transform', `rotate(${angle}, 200, 140)`);

            const angleTol = 15;
            if (Math.abs(angle - discPresets.service) <= angleTol || Math.abs(angle - 360) <= angleTol) {
                const p1 = document.getElementById('d-path-service-in');
                const p2 = document.getElementById('d-path-service-out');
                if (p1) p1.classList.add('flow-active');
                if (p2) p2.classList.add('flow-active');
            } else if (Math.abs(angle - discPresets.backwash) <= angleTol) {
                const p1 = document.getElementById('d-path-backwash-in');
                const p2 = document.getElementById('d-path-backwash-out');
                if (p1) p1.classList.add('flow-active');
                if (p2) p2.classList.add('flow-active');
            } else if (Math.abs(angle - discPresets.brineDraw) <= angleTol) {
                const p1 = document.getElementById('d-path-brineDraw-brine');
                const p2 = document.getElementById('d-path-brineDraw-drain');
                if (p1) p1.classList.add('flow-active');
                if (p2) p2.classList.add('flow-active');
            } else if (Math.abs(angle - discPresets.fastRinse) <= angleTol) {
                const p1 = document.getElementById('d-path-fastRinse-in');
                const p2 = document.getElementById('d-path-fastRinse-out');
                if (p1) p1.classList.add('flow-active');
                if (p2) p2.classList.add('flow-active');
            } else if (Math.abs(angle - discPresets.refill) <= angleTol) {
                const p = document.getElementById('d-path-refill');
                if (p) p.classList.add('flow-active');
            }
        }
    }

    // Switch buttons
    btnMechPiston.addEventListener('click', () => {
        currentMech = 'piston';
        btnMechPiston.classList.add('active');
        btnMechDisc.classList.remove('active');
        svgPistonSim.style.display = 'block';
        svgDiscSim.style.display = 'none';

        lblSimCtrlSlider.innerText = '手动微调：活塞行程位置';
        lblSimCtrlSliderEn.innerText = 'Manual Control: Piston Stroke';

        const stageVal = pistonPresets[currentSimStage];
        valveSlider.value = stageVal;
        sliderValText.innerText = `${stageVal}%`;
        updateFlowPaths('piston', stageVal);
    });

    btnMechDisc.addEventListener('click', () => {
        currentMech = 'disc';
        btnMechDisc.classList.add('active');
        btnMechPiston.classList.remove('active');
        svgDiscSim.style.display = 'block';
        svgPistonSim.style.display = 'none';

        lblSimCtrlSlider.innerText = '手动微调：瓷盘旋转角度';
        lblSimCtrlSliderEn.innerText = 'Manual Control: Disc Rotation';

        const angle = discPresets[currentSimStage];
        const pct = Math.round((angle / 360) * 100);
        valveSlider.value = pct;
        sliderValText.innerText = `${angle}°`;
        updateFlowPaths('disc', pct);
    });

    // Slider inputs
    valveSlider.addEventListener('input', (e) => {
        const pct = parseInt(e.target.value);
        if (currentMech === 'piston') {
            sliderValText.innerText = `${pct}%`;
        } else {
            const angle = Math.round((pct / 100) * 360);
            sliderValText.innerText = `${angle}°`;
        }

        // Detect proximity to snap to cycle active classes
        let activeStage = null;
        const presets = currentMech === 'piston' ? pistonPresets : discPresets;
        const targetVal = currentMech === 'piston' ? pct : Math.round((pct / 100) * 360);
        const tolerance = currentMech === 'piston' ? 6 : 15;

        Object.keys(presets).forEach(stage => {
            if (Math.abs(targetVal - presets[stage]) <= tolerance) {
                activeStage = stage;
            }
        });

        cycleBtns.forEach(btn => {
            if (btn.dataset.simStage === activeStage) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });

        if (activeStage) currentSimStage = activeStage;
        updateFlowPaths(currentMech, pct);
    });

    // Cycle selection buttons
    cycleBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            cycleBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            currentSimStage = btn.dataset.simStage;
            const presets = currentMech === 'piston' ? pistonPresets : discPresets;
            const val = presets[currentSimStage];

            if (currentMech === 'piston') {
                valveSlider.value = val;
                sliderValText.innerText = `${val}%`;
                updateFlowPaths('piston', val);
            } else {
                const pct = Math.round((val / 360) * 100);
                valveSlider.value = pct;
                sliderValText.innerText = `${val}°`;
                updateFlowPaths('disc', pct);
            }
        });
    });

    // Trigger initial state
    btnMechPiston.click();
}

// ==========================================
// INITIALIZE PAGE
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
    initAnatomy();
    initRegenTabs();
    initIonExchangeSimulation();
    initBrandSelector();
    initCalculator();
    initGpgConverter();
    initValveSimulator();
});
