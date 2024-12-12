#   !/bin/bash
ow_deploy_dir=$(find / -type d -name "openwhisk-deploy-kube" 2>/dev/null | head -n 1)

if [[ -n "$ow_deploy_dir" ]]; then
    cd "$ow_deploy_dir"
    path="helm/openwhisk/values.yaml"
    sed -i 's/^ *actionsInvokesPerminute: *[0-9]\+/    actionsInvokesPerminute: 1000/' "$path"
    sed -i 's/^ *actionsInvokesConcurrent: *[0-9]\+/    actionsInvokesConcurrent: 1000/' "$path"
    echo "Updated values in $path:"
    grep -E 'actionsInvokesPerminute|actionsInvokesConcurrent' "$path"
else
    echo "Directory 'ow_deploy' not found."
fi