.PHONY: push build run generate-filetree

push:
	git push origin
	git push gitea

generate-filetree:
	python3 scripts/generate_filetree.py

build: generate-filetree
	hugo --minify

run: generate-filetree
	hugo server -D
