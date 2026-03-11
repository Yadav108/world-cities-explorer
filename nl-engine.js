// ════════════════════════════════════════════════════════════════
//  NL Engine — Natural Language Query Handler
//  Prompt 21 · replaces handleNLQuery() in index.html
//  Depends on globals: COUNTRY_LIST, COUNTRY_ALIASES, extractCountry,
//                      getClassifier, switchMode, CountrySwitcher,
//                      setNLStatus, setStatus, _applyData
// ════════════════════════════════════════════════════════════════

const NLEngine = {

    ranking:   null,
    isReady:   false,

    // ── Concept glossary (explanation handler) ──────────────────
    GLOSSARY: {
        gravity_model: {
            term:       'Gravity Score',
            definition: 'A measure of urban attraction between two cities, adapted from Newton\'s law. Two large nearby cities have a high gravity score; two small distant cities have a low one.',
            formula:    'score = (pop_A × pop_B) / distance_km²',
            example:    'Tokyo ↔ Yokohama: pop 13.9M × 3.7M / 29² = extremely high attraction'
        },
        primacy_index: {
            term:       'Primacy Index',
            definition: 'The share of a country\'s tracked urban population living in its largest city. A high primacy index means one city dominates; a low value means urban power is spread.',
            formula:    'P = population_largest / Σ population_all_cities',
            example:    'Bangkok = 58% of Thailand\'s urban population → P = 0.58 (dominant)'
        },
        haversine: {
            term:       'Haversine Distance',
            definition: 'The great-circle distance between two points on Earth, accounting for the planet\'s curvature. More accurate than Euclidean distance for long distances.',
            formula:    'd = 2R · atan2(√a, √(1−a))  where  a = sin²(Δlat/2) + cos(lat₁)·cos(lat₂)·sin²(Δlng/2)',
            example:    'Berlin (52.5°N, 13.4°E) ↔ Munich (48.1°N, 11.6°E) = 504 km'
        },
        polycentric: {
            term:       'Polycentric / Distributed',
            definition: 'A city network where urban population and economic activity are spread across multiple cities of similar size. No single city dominates.',
            formula:    'Primacy Index < 0.15',
            example:    'Germany: Berlin, Hamburg, Munich, Cologne all compete — P ≈ 0.24'
        },
        monocentric: {
            term:       'Monocentric / Primate City',
            definition: 'A country where one city overwhelmingly dominates urban life, economic activity, and culture. All roads lead to the capital.',
            formula:    'Primacy Index > 0.35',
            example:    'Thailand: Bangkok at 58% — P ≈ 0.58'
        },
        normalization: {
            term:       'Score Normalization',
            definition: 'Raw gravity scores depend on population scale — Germany\'s scores are millions of times larger than Luxembourg\'s. Min-max normalization rescales all scores to 0–1 so countries are comparable.',
            formula:    'normalized = (score − min) / (max − min)',
            example:    'Germany raw: 4.2 × 10¹² → normalized: 1.0 (strongest pair in Germany)'
        }
    },

    // ── Region mapping (recommendation handler) ─────────────────
    REGIONS: {
        europe:   ['Germany','France','Italy','Spain','Poland','Netherlands','Belgium','Sweden',
                   'Norway','Denmark','Finland','Austria','Switzerland','Portugal','Czech Republic',
                   'Romania','Hungary','Greece','Serbia','Bulgaria','Croatia','Slovakia','Slovenia',
                   'Lithuania','Latvia','Estonia','Luxembourg','Iceland','Ireland','United Kingdom',
                   'Albania','Bosnia and Herzegovina','Moldova','Ukraine','Belarus','Russia'],
        asia:     ['China','Japan','India','Indonesia','Pakistan','Bangladesh','Vietnam','Thailand',
                   'Philippines','Myanmar','South Korea','North Korea','Malaysia','Taiwan','Sri Lanka',
                   'Nepal','Cambodia','Laos','Mongolia','Singapore','Kazakhstan','Uzbekistan',
                   'Kyrgyzstan','Tajikistan','Afghanistan','Iran','Iraq','Syria','Lebanon','Jordan',
                   'Israel','Palestine','Saudi Arabia','United Arab Emirates','Oman','Qatar','Kuwait',
                   'Bahrain','Yemen'],
        africa:   ['Nigeria','Ethiopia','Egypt','Tanzania','Kenya','Algeria','Sudan','Morocco',
                   'Ghana','Mozambique','Angola','Cameroon','Ivory Coast','Niger','Mali','Senegal',
                   'Zambia','Zimbabwe','Somalia','Tunisia','Libya','Congo','Rwanda','Uganda',
                   'Burkina Faso','Chad','Botswana','Benin'],
        americas: ['United States','Brazil','Mexico','Colombia','Argentina','Peru','Venezuela',
                   'Chile','Ecuador','Bolivia','Paraguay','Uruguay','Cuba','Haiti','Dominican Republic',
                   'Guatemala','Honduras','El Salvador','Nicaragua','Costa Rica','Panama','Jamaica',
                   'Canada'],
        oceania:  ['Australia','New Zealand']
    },

    // ── Init: load ranking.json ──────────────────────────────────
    async init() {
        try {
            this.ranking = await d3.json('global_ranking.json')
            this.isReady = true
        } catch (e) {
            console.warn('NLEngine: could not load global_ranking.json', e)
            this.isReady = false
        }
    },

    // ── Main entry point called from button / Enter key ──────────
    async process(query) {
        query = (query || '').trim()
        if (!query) return

        const btn = document.getElementById('nl-ask-btn')
        btn.disabled    = true
        btn.textContent = '⏳'

        // hide previous answer
        const box = document.getElementById('nl-answer-box')
        box.style.display = 'none'
        box.innerHTML     = ''

        try {
            const { intent, confidence } = await this._classify(query)
            const entities = this._extractEntities(query)
            await this._route(intent, confidence, query, entities)
        } catch (e) {
            setNLStatus(`❌ ${e.message}`, null)
        }

        btn.disabled    = false
        btn.textContent = '🧠 Ask'
    },

    // ── Classify intent via keyword → ML fallback ────────────────
    async _classify(query) {
        const q = query.toLowerCase()

        // keyword shortcuts (instant, no model needed)
        const conceptKeys = ['what is','what does','explain','define','meaning of','how does','what are gravity','haversine','primacy mean','what\'s a','normaliz']
        const compareKeys = ['vs','versus','compare','more than','less than','greater','between','difference']
        const recKeys     = ['most','least','highest','lowest','best','top country','which country has','find me','show me a country']
        const navKeys     = ['show','go to','switch to','load','open','explore','gravity network','concentration in','gravity in','network in','gravity for']

        if (conceptKeys.some(k => q.includes(k))) return { intent: 'explanation', confidence: 0.95 }
        if (compareKeys.some(k => q.includes(k)) && this._extractEntities(query).countries.length >= 2)
            return { intent: 'comparison', confidence: 0.93 }
        if (recKeys.some(k => q.includes(k))) return { intent: 'recommendation', confidence: 0.90 }
        if (navKeys.some(k => q.includes(k))) return { intent: 'navigation', confidence: 0.92 }

        // check if a single country + known mode keyword → navigation
        const entities = this._extractEntities(query)
        if (entities.countries.length === 1 && entities.mode) return { intent: 'navigation', confidence: 0.88 }
        if (entities.countries.length === 1) return { intent: 'data', confidence: 0.85 }

        // fall back to zero-shot ML model
        try {
            const clf = await getClassifier()
            setNLStatus('🧠 Classifying intent…', null)
            const labels = [
                'comparison between two countries or cities',
                'data question about a specific country statistics',
                'recommendation or finding best matching country',
                'explanation of a concept term or formula',
                'navigate to a country or switch visualization mode'
            ]
            const result = await clf(query, labels, { multi_label: false })
            const intentMap = {
                'comparison between two countries or cities':           'comparison',
                'data question about a specific country statistics':    'data',
                'recommendation or finding best matching country':      'recommendation',
                'explanation of a concept term or formula':             'explanation',
                'navigate to a country or switch visualization mode':   'navigation'
            }
            return {
                intent:     intentMap[result.labels[0]] || 'data',
                confidence: result.scores[0]
            }
        } catch {
            // if model unavailable, guess from entities
            return { intent: entities.countries.length ? 'data' : 'recommendation', confidence: 0.60 }
        }
    },

    // ── Entity extraction ────────────────────────────────────────
    _extractEntities(query) {
        const q = query.toLowerCase()

        // countries (reuse existing COUNTRY_LIST + COUNTRY_ALIASES from index.html)
        const countries = []
        if (typeof COUNTRY_ALIASES !== 'undefined') {
            for (const [alias, name] of Object.entries(COUNTRY_ALIASES)) {
                if (new RegExp(`\\b${alias}\\b`, 'i').test(q) && !countries.includes(name))
                    countries.push(name)
            }
        }
        if (typeof COUNTRY_LIST !== 'undefined') {
            for (const c of COUNTRY_LIST) {
                if (q.includes(c.toLowerCase()) && !countries.includes(c))
                    countries.push(c)
            }
        }

        // mode
        const gravKeys  = ['gravity','network','connect','attract','link','pull','pairs','between cities']
        const concKeys  = ['concentrat','dominat','primacy','primate','distributed','spread','urban hier']
        const mode = gravKeys.some(k => q.includes(k)) ? 'gravity'
                   : concKeys.some(k => q.includes(k)) ? 'concentration'
                   : null

        // region
        let region = null
        for (const [r, countries_] of Object.entries(this.REGIONS)) {
            if (q.includes(r) || (r === 'americas' && (q.includes('america') || q.includes('latin')))) {
                region = r; break
            }
        }

        // superlative
        const superlative = q.includes('most') || q.includes('highest') || q.includes('largest') ? 'most'
                          : q.includes('least') || q.includes('lowest') || q.includes('smallest') ? 'least'
                          : null

        return { countries, mode, region, superlative }
    },

    // ── Route to correct handler ─────────────────────────────────
    async _route(intent, confidence, query, entities) {
        if (confidence < 0.52) {
            this._render({
                type: 'clarification',
                text: 'Not sure what you\'re asking. Try one of these:',
                suggestions: [
                    "What is Japan's primacy index?",
                    'Compare France and Germany',
                    'Most distributed country in Europe',
                    'What does a gravity score mean?',
                    'Show gravity network for India'
                ]
            })
            return
        }

        let result
        switch (intent) {
            case 'data':           result = this._handleData(query, entities);          break
            case 'comparison':     result = this._handleComparison(entities);           break
            case 'recommendation': result = this._handleRecommendation(query, entities); break
            case 'explanation':    result = this._handleExplanation(query);             break
            case 'navigation':     result = await this._handleNavigation(entities);     break
            default:               result = { type: 'error', text: 'Unknown intent — try rephrasing.' }
        }
        this._render(result)
    },

    // ── Handler: data question about one country ─────────────────
    _handleData(query, entities) {
        const country = entities.countries[0] || (typeof extractCountry !== 'undefined' ? extractCountry(query) : null)
        if (!country) return {
            type: 'error',
            text: 'Which country are you asking about? Try: "What is Germany\'s primacy index?"'
        }
        if (!this.ranking) return { type: 'error', text: 'Ranking data not loaded yet.' }
        const entry = this.ranking.find(d => d.country.toLowerCase() === country.toLowerCase())
        if (!entry) return { type: 'error', text: `No data found for "${country}". Check spelling.` }

        return {
            type: 'answer',
            country,
            headline: `${country} — Urban Statistics`,
            facts: [
                { label: 'Primacy Index',  value: (entry.primacy_index * 100).toFixed(1) + '%' },
                { label: 'Urban Pattern',  value: entry.pattern },
                { label: 'Largest City',   value: entry.largest_city || '—' },
                { label: 'Global Rank',    value: `#${entry.rank} of ${this.ranking.length}` },
                { label: 'Cities Tracked', value: entry.total_cities || '—' }
            ],
            insight:  this._generateInsight(entry),
            action:   { label: `Explore ${country} →`, country }
        }
    },

    // ── Handler: compare two countries ──────────────────────────
    _handleComparison(entities) {
        if (entities.countries.length < 2) return {
            type: 'error',
            text: 'I need two countries to compare. Try: "Compare France and Germany"'
        }
        if (!this.ranking) return { type: 'error', text: 'Ranking data not loaded yet.' }
        const [nameA, nameB] = entities.countries.slice(0, 2)
        const a = this.ranking.find(d => d.country === nameA)
        const b = this.ranking.find(d => d.country === nameB)
        if (!a || !b) return { type: 'error', text: `No data for ${!a ? nameA : nameB}.` }

        const more = a.primacy_index > b.primacy_index ? nameA : nameB
        const less = more === nameA ? nameB : nameA
        const diff = Math.abs(a.primacy_index - b.primacy_index)

        return {
            type:     'comparison',
            headline: `${nameA} vs ${nameB}`,
            a, b,
            verdict:  `${more} is more concentrated than ${less} by ${(diff * 100).toFixed(1)} percentage points.`
        }
    },

    // ── Handler: recommendation (most/least + optional region) ───
    _handleRecommendation(query, entities) {
        if (!this.ranking) return { type: 'error', text: 'Ranking data not loaded yet.' }
        let pool = [...this.ranking]

        if (entities.region) {
            const regionCountries = this.REGIONS[entities.region] || []
            pool = pool.filter(d => regionCountries.includes(d.country))
        }

        pool = pool.filter(d => d.confidence === 'high' || !entities.region)

        if (entities.superlative === 'least') {
            pool.sort((a, b) => a.primacy_index - b.primacy_index)
        } else {
            pool.sort((a, b) => b.primacy_index - a.primacy_index)
        }

        const top3 = pool.slice(0, 3)
        if (!top3.length) return { type: 'error', text: 'No results found for that filter.' }

        const qualifier = entities.superlative === 'least' ? 'most distributed' : 'most concentrated'
        const scope     = entities.region ? `in ${entities.region.charAt(0).toUpperCase() + entities.region.slice(1)}` : 'globally'

        return {
            type:     'recommendation',
            headline: `Top 3 ${qualifier} ${scope}`,
            results:  top3.map(d => ({
                country: d.country,
                primacy: d.primacy_index,
                pattern: d.pattern,
                rank:    d.rank
            })),
            action: { label: `Explore ${top3[0].country} →`, country: top3[0].country }
        }
    },

    // ── Handler: explain a concept ───────────────────────────────
    _handleExplanation(query) {
        const q = query.toLowerCase()
        const conceptMap = [
            { keys: ['gravity score','gravity of','gravity mean','gravity model','what is gravity','how is gravity'],   term: 'gravity_model' },
            { keys: ['primacy','primacy index','what is primacy'],                                                       term: 'primacy_index' },
            { keys: ['haversine','distance formula','how is distance','distance calculated'],                            term: 'haversine' },
            { keys: ['polycentric','distributed','what is distributed','what is polycentric'],                           term: 'polycentric' },
            { keys: ['monocentric','dominant city','primate city','what is monocentric'],                                term: 'monocentric' },
            { keys: ['normaliz','normalization','why normalize','what is normalization'],                                 term: 'normalization' }
        ]
        const match = conceptMap.find(c => c.keys.some(k => q.includes(k)))
        if (!match) return {
            type: 'error',
            text: 'I can explain: gravity scores, primacy index, Haversine distance, polycentric, monocentric, normalization.'
        }
        const entry = this.GLOSSARY[match.term]
        return {
            type:       'explanation',
            headline:   entry.term,
            definition: entry.definition,
            formula:    entry.formula,
            example:    entry.example
        }
    },

    // ── Handler: navigate / load country ────────────────────────
    async _handleNavigation(entities) {
        const country = entities.countries[0]
        const mode    = entities.mode

        if (country) {
            if (typeof CountrySwitcher !== 'undefined') {
                CountrySwitcher.selectCountry(country)
            }
            if (mode && typeof switchMode !== 'undefined') {
                setTimeout(() => switchMode(mode), 600)
            }
            return {
                type:    'navigation',
                headline: `Loading ${country}…`,
                country,
                mode
            }
        }

        if (mode && typeof switchMode !== 'undefined') {
            switchMode(mode)
            return {
                type:    'navigation',
                headline: `Switched to ${mode} view`,
                country: null,
                mode
            }
        }

        return { type: 'error', text: 'I couldn\'t find a country or mode to navigate to.' }
    },

    // ── Render result card ───────────────────────────────────────
    _render(result) {
        const box = document.getElementById('nl-answer-box')
        box.innerHTML     = ''
        box.style.display = 'block'

        if (result.type === 'error' || result.type === 'clarification') {
            box.innerHTML = `
            <div class="nl-answer${result.type === 'error' ? ' error' : ''}">
                <div class="nl-answer-text">${result.text}</div>
                ${result.suggestions ? `<div class="nl-suggestions">
                    ${result.suggestions.map(s =>
                        `<span class="nl-suggestion" onclick="NLEngine.process('${s.replace(/'/g, "\\'")}')">${s}</span>`
                    ).join('')}
                </div>` : ''}
            </div>`
            return
        }

        if (result.type === 'answer') {
            box.innerHTML = `
            <div class="nl-answer">
                <div class="nl-answer-headline">${result.headline}</div>
                <div class="nl-facts">
                    ${result.facts.map(f => `
                    <div class="nl-fact">
                        <span class="nl-fact-label">${f.label}</span>
                        <span class="nl-fact-value">${f.value}</span>
                    </div>`).join('')}
                </div>
                <div class="nl-insight">${result.insight}</div>
                ${result.action ? `<button class="nl-action-btn"
                    onclick="CountrySwitcher.selectCountry('${result.action.country.replace(/'/g, "\\'")}')">${result.action.label}</button>` : ''}
            </div>`
            return
        }

        if (result.type === 'comparison') {
            const a = result.a, b = result.b
            box.innerHTML = `
            <div class="nl-answer">
                <div class="nl-answer-headline">${result.headline}</div>
                <div class="nl-compare-grid">
                    <div class="nl-compare-col${a.primacy_index > b.primacy_index ? ' winner' : ''}"
                         onclick="CountrySwitcher.selectCountry('${a.country.replace(/'/g, "\\'")}')">
                        <div class="nl-compare-country">${a.country}</div>
                        <div class="nl-compare-value">${(a.primacy_index * 100).toFixed(1)}%</div>
                        <div class="nl-compare-pattern ${a.pattern}">${a.pattern}</div>
                        <div class="nl-compare-rank">#${a.rank} globally</div>
                    </div>
                    <div class="nl-compare-vs">vs</div>
                    <div class="nl-compare-col${b.primacy_index > a.primacy_index ? ' winner' : ''}"
                         onclick="CountrySwitcher.selectCountry('${b.country.replace(/'/g, "\\'")}')">
                        <div class="nl-compare-country">${b.country}</div>
                        <div class="nl-compare-value">${(b.primacy_index * 100).toFixed(1)}%</div>
                        <div class="nl-compare-pattern ${b.pattern}">${b.pattern}</div>
                        <div class="nl-compare-rank">#${b.rank} globally</div>
                    </div>
                </div>
                <div class="nl-verdict">${result.verdict}</div>
            </div>`
            return
        }

        if (result.type === 'recommendation') {
            box.innerHTML = `
            <div class="nl-answer">
                <div class="nl-answer-headline">${result.headline}</div>
                <div class="nl-rec-list">
                    ${result.results.map((r, i) => `
                    <div class="nl-rec-item" onclick="CountrySwitcher.selectCountry('${r.country.replace(/'/g, "\\'")}')">
                        <span class="nl-rec-rank">#${i + 1}</span>
                        <span class="nl-rec-name">${r.country}</span>
                        <span class="nl-rec-val">${(r.primacy * 100).toFixed(1)}%</span>
                        <span class="nl-compare-pattern ${r.pattern}">${r.pattern}</span>
                    </div>`).join('')}
                </div>
                ${result.action ? `<button class="nl-action-btn"
                    onclick="CountrySwitcher.selectCountry('${result.action.country.replace(/'/g, "\\'")}')">${result.action.label}</button>` : ''}
            </div>`
            return
        }

        if (result.type === 'explanation') {
            box.innerHTML = `
            <div class="nl-answer explanation">
                <div class="nl-answer-headline">📐 ${result.headline}</div>
                <div class="nl-expl-def">${result.definition}</div>
                <div class="nl-expl-formula"><code>${result.formula}</code></div>
                <div class="nl-expl-example">📍 Example: ${result.example}</div>
            </div>`
            return
        }

        if (result.type === 'navigation') {
            box.innerHTML = `
            <div class="nl-answer navigation">
                <div class="nl-answer-headline">🗺 ${result.headline}</div>
                ${result.mode ? `<div class="nl-answer-text" style="color:#aaa;font-size:11px">Mode: ${result.mode}</div>` : ''}
            </div>`
            // auto-hide navigation confirmations after 2s
            setTimeout(() => { box.style.display = 'none' }, 2000)
        }
    },

    // ── Generate narrative insight from ranking entry ─────────────
    _generateInsight(entry) {
        const p = entry.primacy_index
        const pattern = entry.pattern
        const city  = entry.largest_city || 'its largest city'
        const pct   = (p * 100).toFixed(0)

        if (pattern === 'monocentric') {
            return `${city} holds ${pct}% of ${entry.country}'s tracked urban population — a classic primate city pattern where one metropolis dominates economic, cultural, and administrative life.`
        }
        if (pattern === 'polycentric') {
            return `At ${pct}% primacy, ${entry.country} has a distributed urban network. ${city} is the largest node, but several cities share economic weight.`
        }
        return `${entry.country} sits in the transitional zone at ${pct}% primacy — neither fully distributed nor fully dominated by ${city}.`
    }
}
