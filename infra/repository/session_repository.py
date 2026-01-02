from domain.entity.subject import Session, TrialResultSummary
from domain.value_object.condition import Condition
from domain.value_object.time_point import TimePoint
from typing import Optional, List, Dict
from domain.repository.session_repository import SessionRepository as ISessionRepository
from infra.file_system.experiment_file_index import ExperimentFileIndex
from datetime import timedelta
from infra.dto.session_files import FileKind, ExperimentFile
from datetime import datetime
from collections import defaultdict


class SessionRepository(ISessionRepository):
    BODY_SWAY_TOLERANCE = timedelta(minutes=20)
    ZERO = timedelta()

    def __init__(
        self,
        index: ExperimentFileIndex,
    ):
        self.index = index

    def get_session(
        self,
        name: str,
        condition:Condition
    ) -> Session:
        candidates = self.index.scan(name, condition)
        questionnaires = [f for f in candidates.files if f.kind.is_questionnaire]
        body_sways = [f for f in candidates.files if f.kind == FileKind.BODY_SWAY]

        summaries = self._build_trial_summaries(
            questionnaires,
            body_sways,
        )

        if not summaries:
            raise ValueError("成立している試行がありません")

        latest_ts = max(summaries)
        return Session(condition, summaries[latest_ts])

    # -------------------------
    # private methods
    # -------------------------

    def _build_trial_summaries(
        self,
        questionnaires: List[ExperimentFile],
        body_sways: List[ExperimentFile],
    ) -> Dict[datetime, TrialResultSummary]:
        result: Dict[datetime, TrialResultSummary] = {}

        for ts, files in self._group_by_timestamp(questionnaires).items():
            summary = self._try_build_summary(ts, files, body_sways)
            if summary is not None:
                result[ts] = summary

        return result

    def _try_build_summary(
        self,
        ts: datetime,
        questionnaire_files: List[ExperimentFile],
        body_sways: List[ExperimentFile],
    ) -> Optional[TrialResultSummary]:
        ssq_before = self._find_by_kind(questionnaire_files, FileKind.SSQ_BEFORE)
        ssq_after = self._find_by_kind(questionnaire_files, FileKind.SSQ_AFTER)
        fms = self._find_by_kind(questionnaire_files, FileKind.FMS)
        body_sway = self._find_body_sway(ts, body_sways)

        if ssq_before is None:
            return None
        if ssq_after is None:
            return None
        if fms is None:
            return None
        if body_sway is None:
            return None

        return TrialResultSummary(
            ssq_timestamp={
                TimePoint.BEFORE: ssq_before.time_stamp,
                TimePoint.AFTER: ssq_after.time_stamp,
            },
            fms_timestamp=fms.time_stamp,
            body_sway_timestamp=body_sway.time_stamp,
        )

    def _find_body_sway(
        self,
        base_ts: datetime,
        body_sways: List[ExperimentFile],
    ) -> Optional[ExperimentFile]:
        candidates = [
            f
            for f in body_sways
            if self.ZERO <= f.time_stamp - base_ts <= self.BODY_SWAY_TOLERANCE
        ]
        return min(candidates, key=lambda f: f.time_stamp - base_ts, default=None)

    def _group_by_timestamp(
        self,
        files: List[ExperimentFile],
    ) -> Dict[datetime, List[ExperimentFile]]:
        grouped: Dict[datetime, List[ExperimentFile]] = defaultdict(list)
        for f in files:
            grouped[f.time_stamp].append(f)
        return dict(grouped)

    def _find_by_kind(
        self,
        files: List[ExperimentFile],
        kind: FileKind,
    ) -> Optional[ExperimentFile]:
        return next((f for f in files if f.kind == kind), None)


def new_session_repository(file_index:ExperimentFileIndex)->ISessionRepository:
    return SessionRepository(file_index)