def CustomCSS() -> str:
    """Returns the custom CSS for the agent."""

    _CUSTOM_CSS = """
        /* Modern minimalist background */
        body, .gradio-container {
            background: #fafafa !important;
        }

        /* Remove any theme backgrounds */
        .gradio-container *[style*="background-image"] {
            background-image: none !important;
        }

        /* Hide footer */
        footer {
            display: none !important;
        }

        /* Subtle imjoseangel logo watermark */
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

        /* Modern chat window - no borders, clean shadows */
        #chatbot {
            border: none !important;
            border-radius: 16px !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08) !important;
            background-color: white !important;
            overflow: hidden;
        }

        /* Hide the label for the chat input */
        #chatbot .icon-button-wrapper.top-panel {
            display: none !important;
        }

        /* Hide Progress Text in chat */
        #chatbot .progress-text {
            display: none !important;
        }

        /* Smaller text in chat */
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

        /* User message styling - Pastel Blue theme */
        #chatbot .message.user,
        #chatbot .user {
            background-color: #dbeafe !important; /* Pastel blue background */
            color: #1e40af !important; /* Dark blue text for contrast */
            border-radius: 18px 18px 4px 18px !important;
            padding: 12px 16px !important;
            margin: 8px 0 !important;
            box-shadow: 0 2px 8px rgba(219, 234, 254, 0.4) !important;
            border: 1px solid #bfdbfe !important;
        }

        /* Bot message styling - Pastel Orange theme */
        #chatbot .message.bot,
        #chatbot .bot {
            background-color: #fed7aa !important; /* Pastel orange background */
            color: #c2410c !important; /* Dark orange text for contrast */
            border-radius: 18px 18px 18px 4px !important;
            padding: 12px 16px !important;
            margin: 8px 0 !important;
            box-shadow: 0 2px 8px rgba(254, 215, 170, 0.4) !important;
            border: 1px solid #fdba74 !important;
        }

        /* Message text styling */
        #chatbot .message.user p,
        #chatbot .user p {
            color: #1e40af !important; /* Dark blue text */
            margin: 0 !important;
        }

        #chatbot .message.bot p,
        #chatbot .bot p {
            color: #c2410c !important; /* Dark orange text */
            margin: 0 !important;
        }

        /* Modern input field */
        #chat_input {
            border: none !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06) !important;
            background-color: white !important;
            transition: all 0.2s ease !important;
        }

        #chat_input:hover {
            box-shadow: 0 6px 24px rgba(0, 0, 0, 0.1) !important;
        }

        /* Input textarea styling */
        #chat_input textarea,
        #chat_input .multimodal-textbox,
        #chat_input > div {
            background-color: white !important;
            border: none !important;
        }

        /* Focus state */
        #chat_input:focus-within {
            box-shadow: 0 8px 32px rgba(59, 130, 246, 0.15) !important;
            transform: translateY(-1px) !important;
        }

        /* Modern clear button */
        #clear_button {
            border: none !important;
            border-radius: 10px !important;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06) !important;
            background-color: white !important;
            transition: all 0.2s ease !important;
        }

        #clear_button:hover {
            box-shadow: 0 6px 24px rgba(0, 0, 0, 0.12) !important;
            transform: translateY(-1px) !important;
        }
        /* Modern logout button */
        #logout_button {
            border: none !important;
            border-radius: 10px !important;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06) !important;
            background-color: white !important;
            transition: all 0.2s ease !important;
        }

        #logout_button:hover {
            box-shadow: 0 6px 24px rgba(0, 0, 0, 0.12) !important;
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
            color: #666;
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
            color: #000000;
            text-decoration: none;
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
