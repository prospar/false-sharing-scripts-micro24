(
 (nil . (

         ))
 (python-mode . (
                 (fill-column . 100)
                 (flycheck-pylintrc . "setup.cfg")
                 (python-shell-interpreter . "/usr/bin/python3")
                 (python-shell-exec-path   . "/usr/bin/python3")
                 (py-isort-options . '("--settings-path=setup.cfg"))
                 (lsp-pylsp-configuration-sources . ["setup.cfg"])
                 (eval . (add-hook 'before-save-hook
                                   #'lsp-format-buffer nil t))
                 ))

 (python-ts-mode . (
                 (fill-column . 100)
                 (flycheck-pylintrc . "setup.cfg")
                 (python-shell-interpreter . "/usr/bin/python3")
                 (python-shell-exec-path   . "/usr/bin/python3")
                 (py-isort-options . '("--settings-path=setup.cfg"))
                 (lsp-pylsp-configuration-sources . ["setup.cfg"])
                 (eval . (add-hook 'before-save-hook
                                   #'lsp-format-buffer nil t))
                 ))
 )

;; Local Variables:
;; eval: (flycheck-mode -1)
;; End:
