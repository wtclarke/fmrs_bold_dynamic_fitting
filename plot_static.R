library(tidyverse)
library(cowplot)
library(stringr)

theme_set(theme_bw())

dyn_res <- read_csv("figures/fsl_static_fitting_results.csv", show_col_types = FALSE) |>
select(-1) |>
mutate(
method = factor(
method,
levels = c("default analysis", "preproc lw matching", "basis lw matching")
)
)

legend_labels <- function(x) str_wrap(x, width = 12)

mean_p <- dyn_res |>
filter(value_type == "Mean") |>
ggplot(aes(x = Metabolite, y = value, col = method)) +
geom_point() +
facet_wrap(~ field, ncol = 2) +
theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1)) +
ylab("Mean bias (%)") +
xlab("") +
theme(legend.title = element_blank()) +
geom_hline(yintercept = 0) +
scale_color_discrete(labels = legend_labels)

sd_p <- dyn_res |>
filter(value_type == "SD") |>
ggplot(aes(x = Metabolite, y = value, col = method)) +
geom_point() +
facet_wrap(~ field, ncol = 2) +
theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1)) +
ylab("s.d. bias (%)") +
xlab("") +
theme(legend.title = element_blank()) +
scale_color_discrete(labels = legend_labels)

cd_p <- dyn_res |>
filter(value_type == "Cohens d") |>
ggplot(aes(x = Metabolite, y = value, col = method)) +
geom_point() +
facet_wrap(~ field, ncol = 2) +
theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1)) +
ylab("|Cohen's d|") +
xlab("") +
theme(legend.title = element_blank()) +
scale_color_discrete(labels = legend_labels)

plot_grid(mean_p, sd_p, cd_p, nrow = 3, labels = c("A", "B", "C"), align = "v")

ggsave("figures/fsl_static.png", width = 8, height = 8)
