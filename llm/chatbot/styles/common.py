def CustomCSS() -> str:
    """Returns the custom CSS for the agent."""

    _CUSTOM_CSS = """
        /* Respect Gradio's native dark/light mode */
        .dark {
            background: #0b0f19 !important;
            color: #f1f3f4 !important;
        }

        .light {
            background: #ffffff !important;
            color: #1f2937 !important;
        }

        /* Show footer with appropriate styling */
        footer {
            display: none !important;
            background: transparent !important;
            border: none !important;
        }

        .dark footer {
            color: #999 !important;
        }

        .light footer {
            color: #666 !important;
        }

        /* Header logo section */
        .header-logo {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            padding: 35px;
            border-radius: 12px;
            border-left: 4px solid #0369a1;
        }

        .dark .header-logo {
            background: #374151 !important;
            border-left-color: #6b7280 !important;
        }

        .light .header-logo {
            background: #f3f4f6 !important;
            border-left-color: #d1d5db !important;
        }

        /* Header welcome section */
        .header-welcome {
            padding: 32px;
            border-radius: 12px;
            border-left: 4px solid transparent;
        }

        .dark .header-welcome {
            background: linear-gradient(90deg, #1e293b 0%, #334155 100%) !important;
        }

        .light .header-welcome {
            background: linear-gradient(90deg, #f0f9ff 0%, #e0f2fe 100%) !important;
        }

        .header-welcome h1 {
            color: #0369a1 !important;
            margin: 0 0 10px 0 !important;
        }

        .header-welcome p {
            margin: 0 !important;
        }

        .dark .header-welcome p {
            color: #cbd5e1 !important;
        }

        .light .header-welcome p {
            color: #64748b !important;
        }

        /* Subtle logo watermark */
        .gradio-container::after {
            content: '';
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 120px;
            height: 48px;
            background-image: url('/gradio_api/file=assets/logo.png');
            background-repeat: no-repeat;
            background-size: contain;
            opacity: 0.08;
            pointer-events: none;
            z-index: 1;
        }

        /* Chat window - adapts to theme */
        .dark #chatbot {
            border: none !important;
            border-radius: 16px !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
            background-color: #2d2d2d !important;
            overflow: hidden;
        }

        .light #chatbot {
            border: none !important;
            border-radius: 16px !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1) !important;
            background-color: #f9fafb !important;
            overflow: hidden;
        }

        /* Hide unnecessary elements */
        #chatbot .icon-button-wrapper.top-panel,
        #chatbot .progress-text {
            display: none !important;
        }

        /* Chat text size */
        #chatbot .message,
        #chatbot .bot,
        #chatbot .user,
        #chatbot p,
        #chatbot div,
        #chatbot span,
        #chatbot * {
            font-size: 14px !important;
            line-height: 1.5 !important;
        }

        /* User messages - Dark mode */
        .dark #chatbot .message.user,
        .dark #chatbot .user {
            background-color: #1e3a8a !important;
            color: #bfdbfe !important;
            border-radius: 18px 18px 4px 18px !important;
            padding: 12px 16px !important;
            margin: 8px 0 !important;
            box-shadow: 0 2px 8px rgba(30, 58, 138, 0.4) !important;
            border: 1px solid #3b82f6 !important;
        }

        .dark #chatbot .message.user p,
        .dark #chatbot .user p {
            color: #bfdbfe !important;
            margin: 0 !important;
        }

        /* User messages - Light mode */
        .light #chatbot .message.user,
        .light #chatbot .user {
            background-color: #dbeafe !important;
            color: #1e40af !important;
            border-radius: 18px 18px 4px 18px !important;
            padding: 12px 16px !important;
            margin: 8px 0 !important;
            box-shadow: 0 2px 8px rgba(30, 64, 175, 0.2) !important;
            border: 1px solid #3b82f6 !important;
        }

        .light #chatbot .message.user p,
        .light #chatbot .user p {
            color: #1e40af !important;
            margin: 0 !important;
        }

        /* Bot messages - Dark mode */
        .dark #chatbot .message.bot,
        .dark #chatbot .bot {
            background-color: #9a3412 !important;
            color: #fed7aa !important;
            border-radius: 18px 18px 18px 4px !important;
            padding: 12px 16px !important;
            margin: 8px 0 !important;
            box-shadow: 0 2px 8px rgba(154, 52, 18, 0.4) !important;
            border: 1px solid #ea580c !important;
        }

        .dark #chatbot .message.bot p,
        .dark #chatbot .bot p {
            color: #fed7aa !important;
            margin: 0 !important;
        }

        /* Bot messages - Light mode */
        .light #chatbot .message.bot,
        .light #chatbot .bot {
            background-color: #fed7aa !important;
            color: #9a3412 !important;
            border-radius: 18px 18px 18px 4px !important;
            padding: 12px 16px !important;
            margin: 8px 0 !important;
            box-shadow: 0 2px 8px rgba(154, 52, 18, 0.2) !important;
            border: 1px solid #ea580c !important;
        }

        .light #chatbot .message.bot p,
        .light #chatbot .bot p {
            color: #9a3412 !important;
            margin: 0 !important;
        }

        /* Input field - Dark mode */
        .dark #chat_input {
            border: none !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3) !important;
            background-color: #374151 !important;
            transition: all 0.2s ease !important;
        }

        .dark #chat_input:hover {
            box-shadow: 0 6px 24px rgba(0, 0, 0, 0.4) !important;
        }

        .dark #chat_input:focus-within {
            box-shadow: 0 8px 32px rgba(96, 165, 250, 0.25) !important;
            transform: translateY(-1px) !important;
        }

        .dark #chat_input textarea,
        .dark #chat_input .multimodal-textbox,
        .dark #chat_input > div,
        .dark #chat_input input,
        .dark #chat_input * {
            background-color: #374151 !important;
            color: #f9fafb !important;
            border: none !important;
        }

        /* Input field - Light mode */
        .light #chat_input {
            border: none !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1) !important;
            background-color: #ffffff !important;
            transition: all 0.2s ease !important;
        }

        .light #chat_input:hover {
            box-shadow: 0 6px 24px rgba(0, 0, 0, 0.15) !important;
        }

        .light #chat_input:focus-within {
            box-shadow: 0 8px 32px rgba(96, 165, 250, 0.25) !important;
            transform: translateY(-1px) !important;
        }

        .light #chat_input textarea,
        .light #chat_input .multimodal-textbox,
        .light #chat_input > div,
        .light #chat_input input,
        .light #chat_input * {
            background-color: #ffffff !important;
            color: #1f2937 !important;
            border: 1px solid #d1d5db !important;
        }

        /* Buttons - Dark mode */
        .dark #clear_button,
        .dark #logout_button {
            border: none !important;
            border-radius: 10px !important;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3) !important;
            background-color: #4b5563 !important;
            color: #f9fafb !important;
            transition: all 0.2s ease !important;
        }

        .dark #clear_button:hover,
        .dark #logout_button:hover {
            background-color: #6b7280 !important;
            box-shadow: 0 6px 24px rgba(0, 0, 0, 0.4) !important;
            transform: translateY(-1px) !important;
        }

        /* Buttons - Light mode */
        .light #clear_button,
        .light #logout_button {
            border: none !important;
            border-radius: 10px !important;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1) !important;
            background-color: #f3f4f6 !important;
            color: #374151 !important;
            transition: all 0.2s ease !important;
        }

        .light #clear_button:hover,
        .light #logout_button:hover {
            background-color: #e5e7eb !important;
            box-shadow: 0 6px 24px rgba(0, 0, 0, 0.15) !important;
            transform: translateY(-1px) !important;
        }
    """

    return _CUSTOM_CSS


def FooterCSS() -> str:
    """Returns the custom CSS for the footer."""

    _FOOTER_CSS = """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <style>
        .imjoseangel-footer {
            color: #999;
            font-size: 12px;
            display: block;
            position: relative;
            width: 100%;
            text-align: center;
            margin-top: 20px;
            font-family: 'Roboto', sans-serif;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }
        .imjoseangel-footer a {
            color: #e5e5e5;
            text-decoration: none;
            transition: color 0.2s ease;
        }
        .imjoseangel-footer a:hover {
            color: #60a5fa;
        }
        .imjoseangel-footer .fa-heart {
            color: #E90606;
            margin: 0 3px;
            font-size: 10px;
            animation: pound .35s infinite alternate;
            -webkit-animation: pound .35s infinite alternate;
        }
        @-webkit-keyframes pound {
            to {
                transform: scale(1.1);
            }
        }
        @keyframes pound {
            to {
                transform: scale(1.1);
            }
        }
        </style>
        <span class="imjoseangel-footer">
            Made with <i class="fa-solid fa-heart"></i> by
            <a href="#" target="_blank">imjoseangel</a>
        </span>
    """

    return _FOOTER_CSS


def AuthHTML() -> str:
    """Returns the custom HTML for the Auth Screen."""

    _AUTH_HTML = """
        <div style="text-align: center; padding: 40px 20px; font-family: 'Roboto', sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center;">
            <div style="margin-bottom: 30px; display: flex; justify-content: center; align-items: center; width: 100%;">
                <img src="/gradio_api/file=assets/logo.png"
                    style="width: auto; height: 80px; max-width: 300px; display: block; margin: 0 auto;"
                    alt="imjoseangel Logo" />
            </div>
            <h2 style="color: #0369a1; margin: 20px 0; font-weight: 500; text-align: center;">
                🤖 AI-Powered Chatbot
            </h2>
            <p style="color: #666; margin-bottom: 30px; font-size: 16px; text-align: center;">
                Please sign in to access your smart assistant
            </p>
            <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #e5e7eb; width: 100%; text-align: center;">
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
                <style>
                .imjoseangel-auth-footer {
                    color: #666;
                    font-size: 14px;
                    font-family: 'Roboto', sans-serif;
                    -webkit-font-smoothing: antialiased;
                    -moz-osx-font-smoothing: grayscale;
                    text-align: center;
                }
                .imjoseangel-auth-footer a {
                    color: #0369a1;
                    text-decoration: none;
                    font-weight: 500;
                }
                .imjoseangel-auth-footer .fa-heart {
                    color: #E90606;
                    margin: 0 3px;
                    font-size: 12px;
                    animation: pound .35s infinite alternate;
                    -webkit-animation: pound .35s infinite alternate;
                }
                h2.svelte-1ogxbi0 {
                    display: none !important;
                }
                @-webkit-keyframes pound {
                    to {
                        transform: scale(1.1);
                    }
                }
                @keyframes pound {
                    to {
                        transform: scale(1.1);
                    }
                }
                </style>
                <span class="imjoseangel-auth-footer">
                    Made with <i class="fa-solid fa-heart"></i> by
                    <a href="#" target="_blank">imjoseangel</a>
                </span>
            </div>
        </div>
    """

    return _AUTH_HTML
