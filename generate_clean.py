import json

# 读取数据
with open('ltv_data_with_arpu.json', 'r', encoding='utf-8') as f:
    data_str = f.read()

# 读取ECharts
with open('echarts_full.js', 'r', encoding='utf-8') as f:
    echarts_js = f.read()

# 生成干净的HTML文件
html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>机甲安卓 · 买量 vs 渠道 LTV倍率分析</title>
<script>{echarts_js}</script>
<style>
.auth-overlay{{position:fixed;top:0;left:0;width:100%;height:100%;background:#0d1117;z-index:9999;display:flex;align-items:center;justify-content:center}}
.auth-box{{background:#111827;border:1px solid #1e2535;border-radius:12px;padding:32px;text-align:center;min-width:350px}}
.auth-box h2{{color:#f1f5f9;font-size:18px;margin-bottom:8px;font-weight:700}}
.auth-box p{{color:#64748b;font-size:13px;margin-bottom:24px;line-height:1.6}}
.auth-input{{width:100%;padding:12px 16px;background:#0d1117;border:1px solid #1e2535;border-radius:8px;color:#e2e8f0;font-size:14px;margin-bottom:16px;text-align:center;letter-spacing:2px}}
.auth-input:focus{{outline:none;border-color:#60a5fa}}
.auth-input.error{{border-color:#f87171;animation:shake 0.5s}}
.auth-btn{{width:100%;padding:12px;background:#1d4ed8;color:#fff;border:none;border-radius:8px;font-size:14px;font-weight:600;cursor:pointer;transition:all 0.2s}}
.auth-btn:hover{{background:#1e40af}}
.auth-error{{color:#f87171;font-size:12px;margin-top:8px;min-height:16px}}
.content-wrapper{{display:none}}
@keyframes shake{{0%,100%{{transform:translateX(0)}}25%{{transform:translateX(-5px)}}75%{{transform:translateX(5px)}}}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;background:#0d1117;color:#e2e8f0;min-height:100vh}}
.header{{padding:28px 36px 20px;border-bottom:1px solid #1e2535}}
.header h1{{font-size:20px;font-weight:700;color:#f1f5f9}}
.header p{{margin-top:5px;font-size:12px;color:#475569}}
.chart-section{{padding:0 36px 36px}}
.tabs{{display:flex;gap:4px}}
.tab{{padding:8px 16px;border-radius:8px 8px 0 0;font-size:12px;cursor:pointer;border:1px solid transparent;border-bottom:none;color:#64748b;transition:all .2s}}
.tab.active{{background:#111827;border-color:#1e2535;color:#f1f5f9}}
.tab:hover:not(.active){{color:#94a3b8}}
.chart-panel{{display:none;background:#111827;border:1px solid #1e2535;border-radius:0 10px 10px 10px;padding:20px}}
.chart-panel.active{{display:block}}
.chart-title{{font-size:14px;font-weight:700;color:#f1f5f9;margin-bottom:3px}}
.chart-desc{{font-size:11px;color:#64748b;margin-bottom:14px;line-height:1.6}}
.chart-box{{width:100%;height:380px}}
</style>
</head>
<body>

<div class="auth-overlay" id="authOverlay">
  <div class="auth-box">
    <h2>🔒 数据访问验证</h2>
    <p>此报告包含内部分析数据<br>请输入访问密码继续查看</p>
    <input type="password" class="auth-input" id="passwordInput" placeholder="请输入访问密码" maxlength="20">
    <button class="auth-btn" onclick="checkPassword()">验证访问</button>
    <div class="auth-error" id="authError"></div>
  </div>
</div>

<div class="content-wrapper" id="contentWrapper">
  <div class="header">
    <h1>机甲安卓 · 买量 vs 渠道 LTV倍率分析</h1>
    <p>数据周期：第1天 — 第720天 | LTV倍率 = LTV_n ÷ LTV_Day1</p>
  </div>

  <div class="chart-section">
    <div class="tabs">
      <div class="tab active" onclick="switchTab(0)">① LTV倍率对比</div>
      <div class="tab" onclick="switchTab(1)">② 倍率差值走势</div>
      <div class="tab" onclick="switchTab(2)">③ LTV绝对值</div>
      <div class="tab" onclick="switchTab(3)">④ 付费率对比</div>
      <div class="tab" onclick="switchTab(4)">⑤ ARPU对比</div>
    </div>

    <div class="chart-panel active" id="panel-0">
      <div class="chart-title">LTV 倍率对比（渠道 vs 买量）</div>
      <div class="chart-desc">重点关注Day205前后的交叉变化</div>
      <div class="chart-box" id="chart0"></div>
    </div>

    <div class="chart-panel" id="panel-1">
      <div class="chart-title">LTV 倍率差值（渠道倍率 − 买量倍率）</div>
      <div class="chart-desc">绿色=渠道领先，红色=买量领先</div>
      <div class="chart-box" id="chart1"></div>
    </div>

    <div class="chart-panel" id="panel-2">
      <div class="chart-title">累计 LTV 绝对值（元/人）</div>
      <div class="chart-desc">买量基数高但渠道增速快</div>
      <div class="chart-box" id="chart2"></div>
    </div>

    <div class="chart-panel" id="panel-3">
      <div class="chart-title">每日付费率对比（%）</div>
      <div class="chart-desc">买量付费率高但渠道趋势更稳</div>
      <div class="chart-box" id="chart3"></div>
    </div>

    <div class="chart-panel" id="panel-4">
      <div class="chart-title">ARPU对比（元/人）</div>
      <div class="chart-desc">🔑 渠道用户单次付费更高，体现长期价值</div>
      <div class="chart-box" id="chart4"></div>
    </div>
  </div>
</div>

<script>
const PASSWORD = 'idswr2026';
let charts = [];

function checkPassword() {{
  const passwordInput = document.getElementById('passwordInput');
  const authOverlay = document.getElementById('authOverlay');
  const contentWrapper = document.getElementById('contentWrapper');
  const authError = document.getElementById('authError');

  if (passwordInput.value.trim() === PASSWORD) {{
    authOverlay.style.display = 'none';
    contentWrapper.style.display = 'block';
    setTimeout(initCharts, 300);
  }} else {{
    passwordInput.classList.add('error');
    authError.textContent = '密码错误，请重新输入';
    passwordInput.value = '';
    setTimeout(() => passwordInput.classList.remove('error'), 500);
  }}
}}

function switchTab(index) {{
  console.log('Switching to tab:', index);

  document.querySelectorAll('.chart-panel').forEach((panel, i) => {{
    panel.classList.toggle('active', i === index);
  }});

  document.querySelectorAll('.tab').forEach((tab, i) => {{
    tab.classList.toggle('active', i === index);
  }});

  if (charts[index]) {{
    setTimeout(() => charts[index].resize(), 100);
    console.log('Chart', index, 'resized');
  }}
}}

function initCharts() {{
  console.log('Initializing charts...');

  const rawData = {data_str};

  const days = rawData.map(d => d.day);
  const buyRatio = rawData.map(d => d.buy_ltv_ratio);
  const channelRatio = rawData.map(d => d.channel_ltv_ratio);
  const diff = rawData.map(d => d.ltv_ratio_diff);
  const buyLtv = rawData.map(d => d.buy_ltv);
  const channelLtv = rawData.map(d => d.channel_ltv);
  const buyPay = rawData.map(d => d.buy_pay_rate);
  const channelPay = rawData.map(d => d.channel_pay_rate);
  const buyArpu = rawData.map(d => d.buy_arpu);
  const channelArpu = rawData.map(d => d.channel_arpu);

  const BLUE = '#60a5fa', ORANGE = '#fb923c', GREEN = '#34d399', RED = '#f87171';

  const baseOption = {{
    backgroundColor: 'transparent',
    grid: {{ left: 60, right: 30, top: 40, bottom: 50 }},
    xAxis: {{ type: 'category', data: days, axisLabel: {{ fontSize: 10, interval: 59, formatter: v => 'D' + v }} }},
    yAxis: {{ type: 'value', axisLabel: {{ fontSize: 10 }} }},
    tooltip: {{ trigger: 'axis', backgroundColor: '#1e2535', textStyle: {{ color: '#e2e8f0' }} }}
  }};

  try {{
    charts[0] = echarts.init(document.getElementById('chart0'));
    charts[0].setOption({{
      ...baseOption,
      legend: {{ textStyle: {{ color: '#94a3b8' }} }},
      series: [
        {{ name: '买量安卓', type: 'line', data: buyRatio, smooth: true, symbol: 'none', lineStyle: {{ color: BLUE, width: 2 }} }},
        {{ name: '渠道安卓', type: 'line', data: channelRatio, smooth: true, symbol: 'none', lineStyle: {{ color: ORANGE, width: 2 }} }}
      ]
    }});

    charts[1] = echarts.init(document.getElementById('chart1'));
    charts[1].setOption({{
      ...baseOption,
      series: [{{
        name: '倍率差',
        type: 'bar',
        data: diff,
        barMaxWidth: 4,
        itemStyle: {{ color: params => diff[params.dataIndex] >= 0 ? GREEN : RED }}
      }}]
    }});

    charts[2] = echarts.init(document.getElementById('chart2'));
    charts[2].setOption({{
      ...baseOption,
      legend: {{ textStyle: {{ color: '#94a3b8' }} }},
      yAxis: {{ ...baseOption.yAxis, axisLabel: {{ fontSize: 10, formatter: v => v + '元' }} }},
      series: [
        {{ name: '买量LTV', type: 'line', data: buyLtv, smooth: true, symbol: 'none', lineStyle: {{ color: BLUE, width: 2 }} }},
        {{ name: '渠道LTV', type: 'line', data: channelLtv, smooth: true, symbol: 'none', lineStyle: {{ color: ORANGE, width: 2 }} }}
      ]
    }});

    charts[3] = echarts.init(document.getElementById('chart3'));
    charts[3].setOption({{
      ...baseOption,
      legend: {{ textStyle: {{ color: '#94a3b8' }} }},
      yAxis: {{ ...baseOption.yAxis, axisLabel: {{ fontSize: 10, formatter: v => v + '%' }} }},
      series: [
        {{ name: '买量付费率', type: 'line', data: buyPay, smooth: true, symbol: 'none', lineStyle: {{ color: BLUE, width: 2 }} }},
        {{ name: '渠道付费率', type: 'line', data: channelPay, smooth: true, symbol: 'none', lineStyle: {{ color: ORANGE, width: 2 }} }}
      ]
    }});

    charts[4] = echarts.init(document.getElementById('chart4'));
    charts[4].setOption({{
      ...baseOption,
      legend: {{ textStyle: {{ color: '#94a3b8' }} }},
      yAxis: {{ ...baseOption.yAxis, axisLabel: {{ fontSize: 10, formatter: v => v + '元' }} }},
      series: [
        {{ name: '买量ARPU', type: 'line', data: buyArpu, smooth: true, symbol: 'none', lineStyle: {{ color: BLUE, width: 2 }} }},
        {{ name: '渠道ARPU', type: 'line', data: channelArpu, smooth: true, symbol: 'none', lineStyle: {{ color: ORANGE, width: 2 }} }}
      ]
    }});

    console.log('All 5 charts initialized successfully');

  }} catch (error) {{
    console.error('Chart initialization error:', error);
  }}

  window.addEventListener('resize', () => {{
    charts.forEach(chart => chart && chart.resize());
  }});
}}

document.addEventListener('keypress', e => {{
  if (e.key === 'Enter' && document.getElementById('authOverlay').style.display !== 'none') checkPassword();
}});
</script>
</body>
</html>'''

with open('index_clean.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Clean version generated successfully')