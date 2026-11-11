import functools
from runtime.common import guarded, model_path, output_path, page_header, srt_text


@functools.lru_cache(maxsize=1)
def model():
    from faster_whisper import WhisperModel
    # CPU int8 works across GPU generations without depending on CTranslate2 CUDA kernels.
    return WhisperModel(model_path(), device="cpu", compute_type="int8", cpu_threads=8)


@guarded
def transcribe(audio, language, translate):
    if not audio:
        raise ValueError("请先上传音频")
    from faster_whisper.audio import decode_audio
    waveform = decode_audio(audio, sampling_rate=16000)
    if len(waveform) > 16000 * 600:
        raise ValueError("单次最多 10 分钟音频，请先分段")
    mapping = {"自动识别": None, "中文": "zh", "英文": "en", "日文": "ja"}
    segments, info = model().transcribe(waveform, language=mapping[language], task="translate" if translate else "transcribe", beam_size=5, vad_filter=False)
    records = [{"start": s.start, "end": s.end, "text": s.text} for s in segments]
    text = "\n".join(record["text"].strip() for record in records)
    txt = output_path(".txt")
    subtitles = output_path(".srt")
    txt.write_text(text, encoding="utf-8")
    subtitles.write_text(srt_text(records), encoding="utf-8")
    return text, str(txt), str(subtitles), f"识别语言：{info.language}；字幕段数：{len(records)}"


def build_ui():
    import gradio as gr
    with gr.Blocks(title="Whisper 字幕") as ui:
        page_header()
        gr.Markdown("默认 CPU INT8，可无卡使用；支持上传录音或麦克风录制。")
        audio = gr.Audio(type="filepath", label="音频（最多10分钟）")
        language = gr.Dropdown(["自动识别", "中文", "英文", "日文"], value="自动识别", label="语言")
        translate = gr.Checkbox(label="翻译为英文字幕", value=False)
        button = gr.Button("转写字幕", variant="primary")
        text = gr.Textbox(label="识别文字", lines=10)
        txt = gr.File(label="下载 TXT")
        srt = gr.File(label="下载 SRT")
        status = gr.Textbox(label="完成信息")
        button.click(transcribe, [audio, language, translate], [text, txt, srt, status], api_name="transcribe")
    return ui
