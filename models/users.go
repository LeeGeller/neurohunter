package models

type HardConstraints struct {
	Salary                    *int     `json:"salary"`
	ExperienceYears           *float64 `json:"experience_years"`
	Education                 *string  `json:"education"`
	NightWorkTolerance        *string  `json:"night_work_tolerance"`
	BusinessTripTolerance     *string  `json:"business_trip_tolerance"`
	WorkFormats               []string `json:"work_formats"`
	PhysicalActivityTolerance *string  `json:"physical_activity_tolerance"`
}

type UserFeature struct {
	UserID          string          `json:"user_id"`
	JobTitles       []string        `json:"job_titles"`
	HardConstraints HardConstraints `json:"hard_constraints"`
}

type JobTitleGroups map[string][]string
