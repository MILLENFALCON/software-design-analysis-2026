WORKFLOW ResumeOptimization

CONFIG:
    SCORE_THRESHOLD: 85
    MAX_ITERATION: 2

STEP 1:
AGENT: GrammarAgent
TASK: spell_check
TASK: grammar_check
TASK: style_consistency
MODE: detailed
OUTPUT: grammar_report

STEP 2:
AGENT: ContentAgent
TASK: expand_projects
TASK: generate_STAR
TASK: add_certifications
MODE: detailed
INPUT: grammar_report
OUTPUT: content_report

STEP 3:
AGENT: FormatAgent
TASK: unify_format
TASK: bullet_point_normalization
TASK: generate_sections
MODE: standard
INPUT: content_report
OUTPUT: formatted_resume

STEP 4:
AGENT: ScoreAgent
TASK: ats_scoring
TASK: readability_analysis
INPUT: formatted_resume
OUTPUT: score_report

IF overall_score < SCORE_THRESHOLD:
    GOTO STEP 2

STEP 5:
AGENT: ReviewerAgent
TASK: consistency_check
TASK: duplicate_detection
INPUT: formatted_resume
OUTPUT: review_report

STEP 6:
AGENT: ExportAgent
TASK: export_txt
INPUT: formatted_resume
OUTPUT: final_resume

END WORKFLOW