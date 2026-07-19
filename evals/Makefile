UV := uv

setup:
	$(UV) sync

eval:
	$(UV) run lynk-evals eval \
		$(if $(TAG),--tag $(TAG)) \
		$(if $(PERSPECTIVE),--perspective $(PERSPECTIVE)) \
		$(if $(CASE),--case $(CASE)) \
		$(if $(REPEAT),--repeat $(REPEAT)) \
		$(if $(LABEL),--label $(LABEL)) \
		$(if $(MODEL),--model $(MODEL)) \
		$(if $(JUDGE_MODEL),--judge-model $(JUDGE_MODEL))

generate:
	$(UV) run lynk-evals generate --perspective $(PERSPECTIVE) --n $(or $(N),10) \
		$(if $(BUSINESS),--business "$(BUSINESS)")

critic:
	$(UV) run lynk-evals critic

review:
	$(UV) run lynk-evals review $(if $(APPROVE),--approve $(APPROVE))

.PHONY: setup eval generate critic review
