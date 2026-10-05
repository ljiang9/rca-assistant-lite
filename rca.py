"""rca-assistant-lite — 故障根因分析。

按现象/时间线引导 5why，列出可能根因与所需证据。零第三方依赖，规则驱动。
"""
from __future__ import annotations

SYMPTOMS = {
    "服务宕机": {
        "whys": ["为什么宕机？进程被杀", "为什么被杀？OOM", "为什么 OOM？内存泄漏",
                 "为什么泄漏？缓存未淘汰", "为什么未淘汰？缺少过期策略"],
        "causes": ["内存泄漏导致 OOM（证据：堆 dump、RSS 曲线）",
                   "发布引入 bug（证据：发布时间线、变更记录）",
                   "依赖数据库不可用拖垮连接池（证据：DB 监控）"],
    },
    "响应慢": {
        "whys": ["为什么慢？P99 升高", "为什么升高？下游调用慢", "为什么下游慢？慢查询",
                 "为什么慢查询？缺索引", "为什么缺索引？表结构变更未评审"],
        "causes": ["数据库慢查询（证据：慢查询日志）",
                   "下游服务限流（证据：限流指标）",
                   "GC 频繁（证据：GC 日志）"],
    },
    "数据错误": {
        "whys": ["为什么错误？金额不对", "为什么不对？单位换算错", "为什么错？混用元/分",
                 "为什么混用？接口契约不一致", "为什么不一致？缺少字段校验"],
        "causes": ["上下游数据契约不一致（证据：报文样例）",
                   "缓存脏数据（证据：缓存 key 与失效时间）",
                   "并发写竞争（证据：并发日志、锁）"],
    },
}


def analyze(symptom: str) -> dict:
    """根据现象给出 5why 链与候选根因。"""
    matched = None
    for key, v in SYMPTOMS.items():
        if key in symptom:
            matched = v
            break
    if matched is None:
        matched = {
            "whys": [f"为什么会出现「{symptom}」？", "上游输入是否异常？",
                     "下游依赖是否异常？", "最近是否有变更？", "资源是否耗尽？"],
            "causes": ["上游输入异常（证据：入参日志）",
                       "下游依赖异常（证据：依赖监控）",
                       "近期变更引入（证据：发布记录）",
                       "资源耗尽（证据：CPU/内存/连接数）"],
        }
    return {"symptom": symptom, "five_whys": matched["whys"],
            "possible_causes": matched["causes"]}


def report(symptom: str) -> str:
    r = analyze(symptom)
    lines = [f"=== 根因分析：{r['symptom']} ===", "5 Why："]
    for i, w in enumerate(r["five_whys"], 1):
        lines.append(f"  {i}. {w}")
    lines.append("候选根因与证据：")
    for c in r["possible_causes"]:
        lines.append(f"  - {c}")
    return "\n".join(lines)
