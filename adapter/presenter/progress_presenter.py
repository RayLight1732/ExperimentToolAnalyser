from application.dto.progress_phase import ProgressPhase
from application.dto.inferential_analysis_step import InferentialAnalysisStep
from application.port.output.progress_output_port import (
    ProgressAdvanceOutputPort,
    ProgressLifeCycleOutputPort,
)
from typing import Dict
import sys


class ProgressPresenter(ProgressAdvanceOutputPort, ProgressLifeCycleOutputPort):
    BAR_WIDTH = 30

    def __init__(self):
        self.phase_to_line: Dict[ProgressPhase, int] = {}
        self.lines = 0

    def on_advanced(self, phase: ProgressPhase, current: int, total: int):
        # 初めて見るフェーズなら新しい行を割り当てる
        if phase not in self.phase_to_line:
            self.phase_to_line[phase] = self.lines
            self.lines += 1
            print()  # 行を1つ確保

        line = self.phase_to_line[phase]

        self._move_cursor_to(line)
        self._draw_line(phase, current, total)
        self._restore_cursor()

    def on_started(self, category: InferentialAnalysisStep):
        pass

    def on_finished(self, category: InferentialAnalysisStep):
        if category == InferentialAnalysisStep.POST_PROCESS:
            self._finish()

    def on_error(self, exception: Exception):
        pass

    # -------- 内部処理 --------

    def _draw_line(self, phase, current, total):
        ratio = current / total
        filled = int(self.BAR_WIDTH * ratio)

        bar = "█" * filled + "░" * (self.BAR_WIDTH - filled)
        percent = ratio * 100

        sys.stdout.write(
            f"\r{phase.name:12} [{bar}] {percent:6.2f}% ({current}/{total})"
        )
        sys.stdout.flush()

    def _move_cursor_to(self, target_line):
        # カーソルを一番下にいると仮定して、そこから上へ
        lines_up = self.lines - 1 - target_line
        if lines_up > 0:
            sys.stdout.write(f"\033[{lines_up}A")  # カーソルを上へ

    def _restore_cursor(self):
        # カーソルを一番下の空行に戻す
        sys.stdout.write(f"\033[{self.lines}B")
        sys.stdout.flush()

    def _finish(self):
        """
        すべての進捗表示が終わった後に必ず呼ぶ。
        次の print() が上書きされないように改行で確定する。
        """
        if self.lines > 0:
            sys.stdout.write("\n")
            sys.stdout.flush()
            self.finished = True
