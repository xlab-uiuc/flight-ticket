#!/usr/bin/env bash
# Install the pinned upstream chart with SREGym's multiarch image/runtime profile.
# Extra arguments are passed to Helm (for example --kubeconfig or --set).
set -euo pipefail

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
chart_revision=146d24925564e2871f4cc6506d4e92098968457d
chart_dir=$(mktemp -d "${TMPDIR:-/tmp}/sregym-openwhisk.XXXXXXXX")
trap 'rm -rf -- "$chart_dir"' EXIT

git -C "$chart_dir" init --quiet
git -C "$chart_dir" remote add origin https://github.com/apache/openwhisk-deploy-kube.git
git -C "$chart_dir" fetch --quiet --depth=1 origin "$chart_revision"
git -C "$chart_dir" checkout --quiet --detach FETCH_HEAD
git -C "$chart_dir" apply "$script_dir/openwhisk/catalog.patch"
cp "$script_dir/openwhisk/runtimes.json" "$chart_dir/helm/openwhisk/sregym-runtimes.json"

helm upgrade --install owdev "$chart_dir/helm/openwhisk" \
    --namespace openwhisk --create-namespace \
    --values "$script_dir/openwhisk/values.yaml" "$@"
